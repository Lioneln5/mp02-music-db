import sqlite3

def build_database(conn):
    """Create the four-table music schema with FK enforcement."""
    conn.execute("PRAGMA foreign_keys = ON;")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Artist (
            artist_id   INTEGER PRIMARY KEY,
            name        TEXT    NOT NULL,
            genre       TEXT    NOT NULL,
            origin_city TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Track (
            track_id         INTEGER PRIMARY KEY,
            title            TEXT    NOT NULL,
            duration_seconds INTEGER NOT NULL,
            artist_id        INTEGER NOT NULL
                REFERENCES Artist(artist_id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Playlist (
            playlist_id   INTEGER PRIMARY KEY,
            playlist_name TEXT    NOT NULL,
            owner_name    TEXT    NOT NULL
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS PlaylistTrack (
            playlist_id INTEGER NOT NULL REFERENCES Playlist(playlist_id),
            track_id    INTEGER NOT NULL REFERENCES Track(track_id),
            position    INTEGER NOT NULL,
            PRIMARY KEY (playlist_id, track_id)
        )
    """)
    
    conn.commit()

def seed_database(conn):
    """Populate all four tables with pop music data."""
    
    conn.executemany(
        "INSERT OR IGNORE INTO Artist (artist_id, name, genre, origin_city) VALUES (?, ?, ?, ?);",
        [
            (1, "Taylor Swift",  "Pop", "Nashville"),
            (2, "Ariana Grande", "Pop", "Boca Raton"),
            (3, "Kenshi Yonezu", "J-Pop", "Tokushima"),
            (4, "Miku Sawai",    "J-Pop", "Tokyo"),
            (5, "Lady Gaga",     "Pop", "New York City"),
            (6, "Madison Beer",  "Pop", "Jericho"),
            (7, "Billie Eilish", "Pop", "Los Angeles"),
        ]
    )

    conn.executemany(
        "INSERT OR IGNORE INTO Track (track_id, title, duration_seconds, artist_id) VALUES (?, ?, ?, ?);",
        [
            (1,  "Shake It Off",       219, 1),
            (2,  "Blank Space",        231, 1),
            (3,  "Anti-Hero",          200, 1),
            (4,  "Love Story",         235, 1),
            (5,  "7 Rings",            178, 2),
            (6,  "Thank U Next",       207, 2),
            (7,  "Positions",          172, 2),
            (8,  "Lemon",              276, 3),
            (9,  "Flamingo",           258, 3),
            (10, "Kick Back",          193, 3),
            (11, "DAYS",               214, 4),
            (12, "Splash Free",        248, 4),
            (13, "Bad Romance",        294, 5),
            (14, "Poker Face",         237, 5),
            (15, "Shallow",            216, 5),
            (16, "Selfish",            191, 6),
            (17, "Boyshit",            183, 6),
            (18, "Bad Guy",            194, 7),
            (19, "Happier Than Ever",  298, 7),
            (20, "Ocean Eyes",         201, 7),
        ]
    )

    conn.executemany(
        "INSERT OR IGNORE INTO Playlist (playlist_id, playlist_name, owner_name) VALUES (?, ?, ?);",
        [
            (1, "Summer Hits",     "Alex"),
            (2, "Chill Vibes",     "Jordan"),
            (3, "Late Night Drive","Casey"),
            (4, "Throwback Pop",   "Riley"),
        ]
    )

    conn.executemany(
        "INSERT OR IGNORE INTO PlaylistTrack (playlist_id, track_id, position) VALUES (?, ?, ?);",
        [
            #Summer Hits
            (1, 1,  1),   #Shake It Off
            (1, 5,  2),   #7 Rings
            (1, 13, 3),   #Bad Romance
            (1, 14, 4),   #Poker Face
            (1, 16, 5),   #Selfish
            (1, 18, 6),   #Bad Guy
            #Chill Vibes
            (2, 2,  1),   #Blank Space
            (2, 6,  2),   #Thank U Next
            (2, 8,  3),   #Lemon
            (2, 11, 4),   #DAYS
            (2, 20, 5),   #Ocean Eyes
            (2, 19, 6),   #Happier Than Ever
            #Late Night Drive
            (3, 3,  1),   #Anti-Hero
            (3, 7,  2),   #Positions
            (3, 9,  3),   #Flamingo
            (3, 15, 4),   #Shallow
            (3, 17, 5),   #Boyshit
            (3, 12, 6),   #Splash Free
            #Throwback Pop
            (4, 4,  1),   #Love Story
            (4, 10, 2),   #Kick Back
            (4, 13, 3),   #Bad Romance
            (4, 14, 4),   #Poker Face
            (4, 16, 5),   #Selfish
            (4, 11, 6),   #DAYS
        ]
    )

    conn.commit()


if __name__ == "__main__":

    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;") 
    build_database(conn)
    seed_database(conn) 
    # IntegrityError demonstration

    try:

        conn.execute("INSERT INTO Track VALUES (1, 'Ghost Track', 210, 9999)")

    except sqlite3.IntegrityError as e:

        print(f"IntegrityError caught: {e}")

    # Persist to disk

    target = sqlite3.connect("music.db")

    conn.backup(target)

    target.close()

    print("Database written to music.db")
