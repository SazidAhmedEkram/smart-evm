import sqlite3

DB_PATH = "evmDatabase.db"

def get_all_voters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nid, name, dob, constituency, face_encoding, has_voted
        FROM voters
    """)

    rows = cursor.fetchall()
    conn.close()

    voters = []
    for row in rows:
        voters.append({
            "nid": row[0],
            "name": row[1],
            "dob": row[2],
            "constituency": row[3],
            "face": "Registered" if row[4] else "Not Registered",
            "status": "Voted" if row[5] == 1 else "Not Voted"
        })

    return voters
