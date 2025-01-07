import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, Response
import numpy as np
import cv2 as cv
import numpy as np
import tensorflow as tf
import pickle
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
from ultralytics import YOLO
from datetime import date
from datetime import datetime
import pandas as pd
import csv
import joblib


# Defining Flask App
app = Flask(__name__)

nimgs = 10

# Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


# Initializing VideoCapture object to access WebCam
face_detector = YOLO("models/yolov8n-face.pt")
facenet = FaceNet()
encoder = LabelEncoder()
faces_embeddings = np.load("models/face_embeddings.npz")
Y = faces_embeddings['arr_1']
encoder.fit(Y)



# If these directories don't exist, create them
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
        f.write('Name,Roll,Time')


# get a number of total registered users
def totalreg():
    return len(list(np.unique(Y)))


# extract the face from an image
def extract_faces(img):
    try:
            faces = face_detector.predict(img)[0].boxes.xywh
            return faces
    except:
        return []


# Identify face using ML model
def identify_face(image):
    model = pickle.load(open("models/svm_model.pkl", "rb"))
    ypred = facenet.embeddings(image)
    decision = model.predict_proba(ypred)

    confidence = np.max(decision)

    if confidence >= 0.8:
        face_name = model.predict(ypred)
        final_name = encoder.inverse_transform(face_name)[0]
        return final_name
    return 'Unknown'


# Extract info from today's attendance file in attendance folder
def extract_attendance():
    first_names = []
    last_names  =  []
    times = []
    with open('Attendance/Attendance-{}.csv'.format(datetoday), mode='r') as file:
        file_data = file.readlines()
        for row in file_data[1:]:
            name, last, time = row.split(',')
            first_names.append(name)
            last_names.append(last)
            time = time.replace('/n', '')
            times.append(time)

    l = len(first_names)
    return first_names, last_names, times, l


# Add Attendance of a specific user
def add_attendance(name):
    file_names = []
    user_firstname = name.split('_')[0]
    user_lastname = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")

    with open('Attendance/Attendance-{}.csv'.format(datetoday), mode='r') as file:
        file_data = file.readlines()
        for row in file_data:
            file_names.append(row.split(',')[0])
    if user_firstname not in file_names:
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{user_firstname},{user_lastname},{current_time}')


## A function to get names and rol numbers of all users
def getallusers():
    userlist =  list(np.unique(Y))
    first_names = []
    last_names = []
    l = len(userlist)

    for i in userlist:
        first, last = i.split('_')
        first_names.append(first)
        last_names.append(last)

    return userlist, first_names, last_names, l




################## ROUTING FUNCTIONS #########################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/professor')
def professor():
    return render_template('professor.html')

@app.route('/absence')
def absence():
    names, rolls, times, l = extract_attendance()
    return render_template('absence.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2)

@app.route('/start', methods=['GET'])
def start():
    names, rolls, times, l = extract_attendance()

    if 'svm_model.pkl' not in os.listdir('models'):
        return render_template('absence.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2, mess='There is no trained model in the static folder. Please add a new face to continue.')

    ret = True
    cap = cv.VideoCapture(0)
    while ret:
        ret, frame = cap.read()
        faces = extract_faces(frame)
        if len(faces) > 0:
            for face in faces:
                x, y, w, h = face
                x1 = int(x - w / 2)
                y1 = int(y - h / 2)
                x2 = int(x + w / 2)
                y2 = int(y + h / 2)
                img = frame[y1:y2, x1:x2]
                img = cv.resize(img, (160, 160))
                img = np.expand_dims(img, axis=0)

                identified_person = identify_face(img)

                if identified_person != 'Unknown':
                    cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    cv.putText(frame, str(identified_person), (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv.LINE_AA)
                    add_attendance(identified_person)
        cv.imshow('Attendance', frame)
        if cv.waitKey(1) == 27:
            break
    cap.release()
    cv.destroyAllWindows()
    names, rolls, times, l = extract_attendance()
    return render_template('absence.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2)

# Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
