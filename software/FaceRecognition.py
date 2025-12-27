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
                  KEY
                  AUTOINCREMENT,
                  name
                  TEXT
                  NOT
                  NULL,
                  party
                  TEXT
                  NOT
                  NULL,
                  constituency
                  TEXT
                  NOT
                  NULL,
                  candidate_picture
                  BLOB,
                  party_logo
                  BLOB
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

def register_voter(ui):
    print("\n--- VOTER REGISTRATION ---")
    VoiceInstructions.speak("Please scan your face")

    # Open camera
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Cannot open camera")
        VoiceInstructions.speak("Cannot open camera")
        return

    VoiceInstructions.speak("Camera is on. Press Enter to start face capture")
    cv2.namedWindow("Face Registration - Live Feed")
    while True:
        ret, frame = video.read()
        if not ret:
            continue
        cv2.imshow("Face Registration - Live Feed", frame)
        if cv2.waitKey(1) & 0xFF == 13:  # Enter key
            print("Capturing 3 frames for stable registration...")
            time.sleep(1)
            break

    # Capture 3 frames
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
        return

    final_encoding = np.mean(encodings, axis=0)
    VoiceInstructions.speak("Face captured successfully")
    ui.notRegisteredCard.setStyleSheet("background-color: green;")
    ui.notRegistered.setText("Registered")
    ui.validConstituency.setVisible(False)
    ui.validRegister.setVisible(False)
    return final_encoding

def insert_voter_to_db(nid, name, dob, phone, constituency, address, face_encoding):
    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()

    # Check if NID already exists
    c.execute("SELECT * FROM voters WHERE nid=?", (nid,))
    if c.fetchone():
        conn.close()
        return False, "NID already registered!"

    # Check if face already exists
    c.execute("SELECT face_encoding FROM voters")
    all_faces = c.fetchall()
    for f in all_faces:
        known_face = pickle.loads(f[0])
        if face_recognition.compare_faces([known_face], face_encoding, tolerance=0.65)[0]:
            conn.close()
            return False, "This face is already registered with another NID!"

    # Insert voter into DB
    c.execute(
        "INSERT INTO voters (nid, name, dob, phone, constituency, address, face_encoding) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nid, name, dob, phone, constituency, address, pickle.dumps(face_encoding))
    )
    conn.commit()
    conn.close()
    return True, "Voter registered successfully!"



# --- 2. Voting Function (Uses 5-Frame Best Match for Accuracy) ---
def vote():
    print("\n--- VOTING STATION ---")
    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()

    # Open camera
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Cannot open camera")
        VoiceInstructions.speak("Camera cannot be opened. Please contact operator.")
        return None, None, None

    VoiceInstructions.speak("Voting station ready. Camera is on. Press Enter to start face capture for voting.")
    print("Camera is on. Press Enter to start face capture for voting...")

    cv2.namedWindow("Voting - Live Feed")

    # Live preview until user presses Enter
    while True:
        ret, frame = video.read()
        if not ret:
            continue

        cv2.imshow("Voting - Live Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 13:  # Enter pressed
            VoiceInstructions.speak("Face scanning started. Please stay still.")
            print("Capturing multiple frames for best match...")
            break

    # ----------- SCAN 5 FRAMES -----------
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

    VoiceInstructions.speak("Face scanning completed.")

    # ----------- NO FACE FOUND -----------
    if not captured_encodings:
        print("No clear face detected. Vote failed.")
        VoiceInstructions.speak("No face detected. Please try again.")
        video.release()
        cv2.destroyAllWindows()
        conn.close()
        return None, None, None

    # Load DB voters
    c.execute("SELECT nid, name, has_voted, face_encoding FROM voters WHERE face_encoding IS NOT NULL")
    voters = c.fetchall()

    # Load candidates
    c.execute("SELECT id, name, party FROM candidates")
    candidates = c.fetchall()

    best_voter_match = None
    best_distance = 1.0

    # Match faces
    for v in voters:
        db_face = pickle.loads(v[3])
        distances = face_recognition.face_distance(captured_encodings, db_face)
        min_dist_for_this_voter = np.min(distances)

        if min_dist_for_this_voter < best_distance:
            best_distance = min_dist_for_this_voter
            best_voter_match = v

    STRICT_TOLERANCE = 0.50

    # ----------- NOT RECOGNIZED -----------
    if best_distance >= STRICT_TOLERANCE:
        print("Face not recognized.")
        VoiceInstructions.speak("Face not recognized. You are not authorized to vote.")
        video.release()
        cv2.destroyAllWindows()
        conn.close()
        return None, None, "Face not recognized"

    voter = best_voter_match

    # ----------- ALREADY VOTED -----------
    if voter[2] == 1:
        print(f"{voter[1]} has already voted.")
        VoiceInstructions.speak("You have already voted. Multiple voting is not allowed.")
        video.release()
        cv2.destroyAllWindows()
        conn.close()
        return voter[1], voter[0], "Already voted"

    # ----------- VERIFIED -> NOW CLOSE CAMERA -----------
    print(f"Voter verified: {voter[1]} (NID: {voter[0]})")
    VoiceInstructions.speak(f"Voter verified. Welcome {voter[1]}. Please enter the start voting Button.")

    # CLOSE camera here (before showing candidates)
    video.release()
    cv2.destroyAllWindows()
    # macOS FIX — force window event loop to run
    for i in range(5):
        cv2.waitKey(1)

    # Fetch candidates
    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()
    c.execute("SELECT id, name, party FROM candidates")
    candidates = c.fetchall()
    conn.close()

    # # Call new function
    # selected_name, selected_party = show_candidates_and_vote(candidates, voter[0])

    return voter[1], voter[0], "Verified"



def show_candidates_and_vote(candidates, voter_nid):
    """
    Displays candidates, lets voter choose, and records vote.
    Returns selected candidate info.
    """
    import sqlite3
    import VoiceInstructions  # Assuming this module exists

    conn = sqlite3.connect('evmDatabase.db')
    c = conn.cursor()

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
                VoiceInstructions.speak("Invalid candidate. Please try again.")
        except ValueError:
            print("Please enter a number.")
            VoiceInstructions.speak("Please enter a valid number.")

    # Save vote
    c.execute("INSERT INTO votes (nid, candidate_id) VALUES (?, ?)", (voter_nid, choice_id))
    c.execute("UPDATE voters SET has_voted=1 WHERE nid=?", (voter_nid,))
    conn.commit()
    conn.close()

    print(f"Thank you! Your vote for {selected_name} ({selected_party}) has been recorded!")
    VoiceInstructions.speak("Thank you. Your vote has been recorded successfully.")

    return selected_name, selected_party


# --- Example Usage ---
# 1. Run this first to ensure the database and sample candidates exist
#setup_database()

# 2. Uncomment the function you want to run:
# register_voter()
#vote()