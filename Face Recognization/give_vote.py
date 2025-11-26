from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch


def speak(text):
    voice = Dispatch("SAPI.SpVoice")
    voice.Speak(text)


# ---- Paths ----
records_file = 'data/face_records.pkl'

# ---- Check if registered voters exist ----
if not os.path.exists(records_file):
    print("❌ No registered voters found! Please run registration first.")
    exit()

with open(records_file, 'rb') as f:
    face_records = pickle.load(f)

# ---- Prepare face data and NID labels for KNN ----
FACES = np.array([record['face_vector'] for record in face_records])
LABELS = np.array([record['nid'] for record in face_records])

# Train KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# ---- Open webcam and face detector ----
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Background image (optional)
imgBackground = cv2.imread("background.png")
if imgBackground is None:
    imgBackground = np.zeros((850, 1080, 3), dtype=np.uint8)  # blank if no image

# Vote CSV columns
COL_NAMES = ['NID', 'VOTE', 'DATE', 'TIME']


# Check if voter already voted
def check_if_voted(nid):
    try:
        with open("Votes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == nid:
                    return True
    except FileNotFoundError:
        pass
    return False


# Party mapping
party_map = {
    ord('1'): "BNP",
    ord('2'): "Jamat",
    ord('3'): "NCP",
    ord('4'): "GOP"
}

speak("Voting system started. Please show your face to the camera.")

output_nid = None

while True:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output_nid = knn.predict(resized_img)[0]

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output_nid), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    # Display in background
    imgBackground[370:370 + 480, 225:225 + 640] = frame
    cv2.imshow("Bangladesh EVM Voting", imgBackground)
    key = cv2.waitKey(1)

    if output_nid is not None:
        # Check if voter already voted
        if check_if_voted(output_nid):
            speak("YOU HAVE ALREADY VOTED")
            print(f"NID {output_nid} has already voted.")
            break

        # If a party key is pressed
        if key in party_map:
            vote_party = party_map[key]
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

            # Save vote
            file_exists = os.path.isfile("Votes.csv")
            with open("Votes.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(COL_NAMES)
                writer.writerow([output_nid, vote_party, date, timestamp])

            speak(f"YOUR VOTE FOR {vote_party} HAS BEEN RECORDED")
            speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
            print(f"NID {output_nid} voted for {vote_party}")
            break

video.release()
cv2.destroyAllWindows()
