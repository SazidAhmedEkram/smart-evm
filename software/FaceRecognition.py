import cv2
import face_recognition
import sqlite3
import pickle
import time
import numpy as np
import VoterRegistration
import VoiceInstructions
import main

# --- Database Setup (Run once to create tables and sample candidates) ---
def setup_database():
    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()

    # 1. Voters Table
    c.execute("""
              CREATE TABLE IF NOT EXISTS voters
              (
                  nid
                  TEXT
                  PRIMARY
                  KEY,
                  name
                  TEXT,
                  dob
                  TEXT,
                  phone
                  TEXT,
                  constituency
                  TEXT,
                  address
                  TEXT,
                  face_encoding
                  BLOB,
                  has_voted
                  INTEGER
                  DEFAULT
                  0
              )
              """)

    # 2. Candidates Table (Auto candidate updating source)
    c.execute("""
              CREATE TABLE IF NOT EXISTS candidates
              (
                  id
                  INTEGER
                  PRIMARY
                  KEY,
                  name
                  TEXT,
                  party
                  TEXT
              )
              """)

    # 3. Votes Table (To store results separately)
    c.execute("""
              CREATE TABLE IF NOT EXISTS votes
              (
                  id
                  INTEGER
                  PRIMARY
                  KEY,
                  nid
                  TEXT,
                  candidate_id
                  INTEGER,
                  vote_timestamp
                  DATETIME
                  DEFAULT
                  CURRENT_TIMESTAMP
              )
              """)

    # Example Candidates (Insert only if table is empty)
    c.execute("SELECT id FROM candidates")
    if not c.fetchone():
        candidates_data = [
            (1, 'Ms. Khaleda Zia', 'BNP'),
            (2, 'Dr. Shafiqul Islam', 'Jamat'),
            (3, 'Nahid Hossain', 'NCP'),
            (4, 'Vp Noor', 'Gono Odhikar Parishad')
        ]
        c.executemany("INSERT INTO candidates (id, name, party) VALUES (?, ?, ?)", candidates_data)
        print("Initial sample candidates added.")

    conn.commit()
    conn.close()


# --- 1. Voter Registration Function (Uses 3-Frame Average for Stability) ---
def register_voter(ui):
    print("\n--- VOTER REGISTRATION ---")
    VoiceInstructions.speak("Please scan your face")


    nid = ui.nid1.text()
    name = ui.name1.text()
    phone = ui.number1.text()
    address = ui.address1.text()
    dob = ui.dob1.text()
    constituency = ui.comboBox1.currentText()

    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()

    # Check if NID already exists
    c.execute("SELECT * FROM voters WHERE nid=?", (nid,))
    if c.fetchone():
        print("NID already registered!")
        VoiceInstructions.speak("The NID you provide is already registered!")
        conn.close()
        return

    # Open camera and show live feed
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Cannot open camera")
        VoiceInstructions.speak("Cannot open camera")
        conn.close()
        return
    VoiceInstructions.speak("Camera is on. Press Enter to start face capture")

    print("Camera is on. Press Enter to start face capture...")


    cv2.namedWindow("Face Registration - Live Feed")

    # Wait for Enter to start capturing
    while True:
        ret, frame = video.read()
        if not ret:
            continue
        cv2.imshow("Face Registration - Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == 13:  # Enter key
            print("Capturing 3 frames for stable registration...")
            time.sleep(1)
            break

    # Capture 3 frames and average the encoding
    encodings = []
    for i in range(3):
        ret, frame = video.read()
        if not ret:
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
            encodings.append(face_encoding)
            print(f"Captured frame {i + 1}")
        else:
            print(f"No face detected in frame {i + 1}, skipping...")

        time.sleep(0.5)

    video.release()
    cv2.destroyAllWindows()

    if len(encodings) < 2:
        print("Failed to capture enough clear faces. Try again.")
        VoiceInstructions.speak("Failed to capture enough clear faces. Please Try again.")
        conn.close()
        return

    final_encoding = np.mean(encodings, axis=0)

    # Check if face already exists
    c.execute("SELECT face_encoding FROM voters")
    all_faces = c.fetchall()
    for f in all_faces:
        known_face = pickle.loads(f[0])
        if face_recognition.compare_faces([known_face], final_encoding, tolerance=0.65)[0]:
            print("This face is already registered with another NID!")

            VoiceInstructions.speak("This face is already registered with another NID!")

            conn.close()
            return

    # Insert voter into DB
    c.execute(
        "INSERT INTO voters (nid, name, dob, phone, constituency, address, face_encoding) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nid, name, dob, phone, constituency, address, pickle.dumps(final_encoding))
    )
    conn.commit()
    conn.close()
    print("Voter registered successfully!")
    VoiceInstructions.spaek("Voter registered successfully!")
    ui.notRegisteredCard.setStyleSheet("background-color: green;")
    ui.notRegistered.setText("Registered")




# --- 2. Voting Function (Uses 5-Frame Best Match for Accuracy) ---
def vote():
    print("\n--- VOTING STATION ---")
    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()

    # Open camera
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Cannot open camera")
        return

    print("Camera is on. Press Enter to start face capture for voting...")
    cv2.namedWindow("Voting - Live Feed")

    while True:
        ret, frame = video.read()
        if not ret:
            continue
        cv2.imshow("Voting - Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == 13:  # Enter key
            print("Capturing multiple frames for best match...")
            break

    # Capture 5 frames rapidly
    captured_encodings = []
    for i in range(5):
        ret, frame = video.read()
        if not ret:
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
            captured_encodings.append(face_encoding)

        time.sleep(0.1)

    video.release()
    cv2.destroyAllWindows()

    if not captured_encodings:
        print("No clear face detected. Vote failed.")
        conn.close()
        return

    # Load all voters and candidates from database
    c.execute("SELECT nid, name, has_voted, face_encoding FROM voters")
    voters = c.fetchall()

    # Dynamic Candidate Update: Fetching live from DB
    c.execute("SELECT id, name, party FROM candidates")
    candidates = c.fetchall()

    best_voter_match = None
    best_distance = 1.0

    # --- Best Match Comparison Logic ---
    for v in voters:
        db_face = pickle.loads(v[3])

        # Check this voter against ALL captured frames
        distances = face_recognition.face_distance(captured_encodings, db_face)
        min_dist_for_this_voter = np.min(distances)

        if min_dist_for_this_voter < best_distance:
            best_distance = min_dist_for_this_voter
            best_voter_match = v

    # --- Final Decision ---
    STRICT_TOLERANCE = 0.50

    if best_distance >= STRICT_TOLERANCE:
        print(f"Face not recognized! Best match distance was {best_distance:.4f} (Threshold is {STRICT_TOLERANCE}).")
        conn.close()
        return

    # Voter found and recognized (best_distance < 0.50)
    voter = best_voter_match

    if voter[2] == 1:
        print(f"ERROR: {voter[1]} (NID: {voter[0]}) has already voted!")
        conn.close()
        return

    print(f"Voter verified: {voter[1]} (NID: {voter[0]}).")

    # --- Voting Process: Dynamic Candidate Update ---
    print("\n--- CANDIDATES ---")
    candidate_map = {}
    for cand in candidates:
        candidate_id, name, party = cand
        print(f"{candidate_id}. {name} ({party})")
        candidate_map[candidate_id] = (name, party)

    while True:
        try:
            choice_id = int(input("Enter candidate ID to vote: "))
            if choice_id in candidate_map:
                selected_name, selected_party = candidate_map[choice_id]
                break
            else:
                print("Invalid candidate ID. Try again.")
        except ValueError:
            print("Please enter a number.")

    # Store vote and mark voter as has_voted
    c.execute("INSERT INTO votes (nid, candidate_id) VALUES (?, ?)", (voter[0], choice_id))
    c.execute("UPDATE voters SET has_voted=1 WHERE nid=?", (voter[0],))
    conn.commit()
    conn.close()

    print(f"\nThank you {voter[1]}! Your vote for {selected_name} ({selected_party}) has been recorded!")


# --- Example Usage ---
# 1. Run this first to ensure the database and sample candidates exist
#setup_database()

# 2. Uncomment the function you want to run:
# register_voter()
#vote()