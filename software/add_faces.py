import cv2
import pickle
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from win32com.client import Dispatch

def speak(text):
    voice = Dispatch("SAPI.SpVoice")
    voice.Speak(text)

speak("Welcome to the face registration for the upcoming election. Please enter your NID")
# ---- Input NID ----
nid = input("Enter your NID: ")

# ---- Create data folder ----
if not os.path.exists('data/'):
    os.makedirs('data/')

records_file = 'data/face_records.pkl'

# ---- Load existing records ----
if os.path.exists(records_file):
    with open(records_file, 'rb') as f:
        face_records = pickle.load(f)
else:
    face_records = []

# ---- Webcam & face detector ----
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ---- Check if NID already exists ----
for record in face_records:
    if record['nid'] == nid:
        print(f"\n❌ NID {nid} is already registered! Cannot register again.")
        exit()

framesTotal = 51
captureAfterFrame = 2
i = 0
faces_data = []

print("\nPress SPACE to capture images, ESC to exit.\n")

while True:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))
        flat_img = resized_img.flatten()

        # ---- Check if this face is already registered (any NID) ----
        for record in face_records:
            existing_face = record['face_vector'].reshape(1, -1)
            current_face = flat_img.reshape(1, -1)
            similarity = cosine_similarity(existing_face, current_face)[0][0]
            if similarity > 0.9:  # similarity threshold (0-1)
                print(f"\n❌ This face is already registered under NID {record['nid']}!")
                video.release()
                cv2.destroyAllWindows()
                exit()

        # ---- Save face every captureAfterFrame frames ----
        if len(faces_data) <= framesTotal and i % captureAfterFrame == 0:
            faces_data.append(flat_img)
        i += 1

        # ---- Display counter + rectangle ----
        cv2.putText(frame, str(len(faces_data)), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)

    cv2.imshow("Register Face - Press SPACE to capture", frame)
    key = cv2.waitKey(1)
    if key == 27 or len(faces_data) >= framesTotal:
        break

video.release()
cv2.destroyAllWindows()

# ---- Save records ----
for face_vec in faces_data:
    face_records.append({"nid": nid, "face_vector": face_vec})

with open(records_file, 'wb') as f:
    pickle.dump(face_records, f)

print(f"\n✅ Registration complete for NID: {nid}")
print(f"Captured {len(faces_data)} images of your face.")
