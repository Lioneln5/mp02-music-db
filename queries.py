"""
queries.py
==========
CIS 3120 · MP02 — SQL and Database
Author 2 module — all query functions

CONTRACT SUMMARY
----------------
Implement the four functions below exactly as specified.  Every function
accepts a conn argument and returns results as a list of rows (the output
of .fetchall()).  The Integrator's main.py calls these functions and handles
all output formatting — do NOT print inside any of these functions.

REQUIRED (graded):
    ✓ get_playlist_tracks(conn, playlist_name)   — JOIN across 4 tables; ORDER BY position
    ✓ get_tracks_on_no_playlist(conn)             — LEFT JOIN + IS NULL pattern
    ✓ get_most_added_track(conn)                  — GROUP BY + ORDER BY COUNT DESC
    ✓ get_playlist_durations(conn)                — SUM + GROUP BY; result in minutes
    ✓ Isolation  — this module must NOT import from schema_data.py or main.py

IMPORTANT:
    - Do not print anything inside these functions.
    - Do not open a database connection inside these functions.
    - All database access must go through the conn parameter.
    - Column order within each returned row must match the specification below.
"""

import sqlite3


#Function 1
def get_playlist_tracks(conn, playlist_name):
    cursor = conn.cursor()
    query = """
    SELECT T.title, A.name, T.duration_seconds, PT.position
    FROM PlaylistTrack AS PT
    JOIN Track AS T ON PT.track_id = T.track_id
    JOIN Artist AS A ON T.artist_id = A.artist_id
    JOIN Playlist AS P ON PT.playlist_id = P.playlist_id
    WHERE P.playlist_name = ?
    ORDER BY PT.position ASC
    """

    cursor.execute(query, (playlist_name,))
    return cursor.fetchall()
#Function 2
def get_tracks_on_no_playlist(conn):
    cursor = conn.cursor()
    query = """
    SELECT T.title, A.name, T.duration_seconds
    FROM Track AS T
    LEFT JOIN PlaylistTrack AS PT ON T.track_id = PT.track_id
    JOIN Artist AS A ON T.artist_id = A.artist_id
    WHERE PT.track_id IS NULL
    """

    cursor.execute(query)
    return cursor.fetchall()

#Function 3
def get_most_added_track(conn):
    cursor = conn.cursor()
    query = """
    SELECT T.title, A.name, COUNT(*) AS playlist_count
    FROM Track AS T
    JOIN PlaylistTrack AS PT ON T.track_id = PT.track_id
    JOIN Artist AS A ON T.artist_id = A.artist_id
    GROUP BY T.track_id
    ORDER BY playlist_count DESC
    LIMIT 1
    """

    cursor.execute(query)
    return cursor.fetchone()

#Function 4
def get_playlist_durations(conn):
    cursor = conn.cursor()
    query = """
    SELECT P.playlist_name, (SUM(T.duration_seconds) / 60.0) AS total_duration_minutes
    FROM Playlist AS P
    JOIN PlaylistTrack AS PT ON P.playlist_id = PT.playlist_id
    JOIN Track AS T ON PT.track_id = T.track_id
    GROUP BY P.playlist_id
    ORDER BY total_duration_minutes DESC
    """

    cursor.execute(query)
    return cursor.fetchall()
    
