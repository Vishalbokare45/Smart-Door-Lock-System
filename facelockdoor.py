import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import serial
import time
import pyttsx3

q = 1
x = 0
c = 0
m = 0
d = 0

# pehele collecting data face1.py chala, vo 500 imgs capture karega fir ye file chala (see line 97 for more info!)

while q <= 2:
    data_path = r'images'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    Training_data, Labels = [], []

    for i, files in enumerate(onlyfiles):
        image_path = join(data_path, onlyfiles[i])  # Corrected image path
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        Training_data.append(np.asarray(images, dtype=np.uint8))
        # print(i)
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()#Local Binary Pattern Histogram
    model.train(np.asarray(Training_data), np.asarray(Labels))
    print("training complete")
    q += 1

face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 140)
engine.setProperty("volume", 1000)

def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return img, []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))

    return img, roi

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)

        if result[1] < 500:
            confidence = int((1 - (result[1]) / 300) * 100)
            display_string = str(confidence)
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 0))

        if confidence >= 83:
            cv2.putText(image, "unlocked", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
            cv2.imshow('face', image)
            x += 1
        else:
            cv2.putText(image, "locked", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
            cv2.imshow('face', image)
            c += 1
    except:
        cv2.putText(image, "Face not found", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
        cv2.imshow('face', image)
        d += 1
        pass

    if cv2.waitKey(1) == 13 or x == 10 or c == 30 or d == 20:
        break

cap.release()
cv2.destroyAllWindows()

if x >= 5:
    m = 1
    # i think idr tuje com5 mai changes karne hai, jab arduino connect karega tab "com5" 
    # ko change kar aur correct com port ka string daal jo arduino IDE mai dikh ra hai like "com4" etc
    ard = serial.Serial('COM12', 115200)
    time.sleep(5)
    var = 'a'
    c = var.encode()
    speak("Face recognition complete. It is matching with the database. Welcome, sir. ")
    ard.write(c)
    time.sleep(5)
elif c == 30:
    speak("The face is not matching. Please press the doorBell.")
elif d == 20:
    speak("The face is not found. Please try again.")

if m == 1:
    speak("The door is closing.")

print("Code corrected successfully.")
