import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import render_template, redirect, url_for, request, session
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
from app_pack import app, db
from app_pack.models import User, Professor, Student, Admin, Element, Module, Filiere, Department, Semestre, Seance, etud_abs, etud_ses


nimgs = 10



# Initializing VideoCapture object to access WebCam
face_detector = YOLO("app_pack/models/yolov8n-face.pt")
facenet = FaceNet()
encoder = LabelEncoder()
faces_embeddings = np.load("app_pack/models/face_embeddings.npz")
Y = faces_embeddings['arr_1']
encoder.fit(Y)


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
    model = pickle.load(open("app_pack/models/svm_model.pkl", "rb"))
    ypred = facenet.embeddings(image)
    decision = model.predict_proba(ypred)
    print(decision)

    confidence = np.max(decision)
    print(confidence)

    if confidence >= 0.8:
        face_name = model.predict(ypred)
        final_name = encoder.inverse_transform(face_name)[0]
        return final_name
    return 'Unknown'


# Extract info from today's attendance file in attendance folder
def extract_attendance(infos_seance):
    session_date = datetime.now().strftime("%m_%d_%y(%H-%M)")

    students_present = {}

    
    id_session = infos_seance['id_session']
    debut_session = infos_seance['seance_debut']

    with open('Attendance/Session-{}-Date-{}.csv'.format(id_session,debut_session), mode='r') as file:
        file_data = file.readlines()
        for row in file_data[1:]:
            id, nom, prenom, temps = row.split(',')
            temps = temps.replace('/n', '')
            if id not in students_present:
                students_present[id] = {'nom': nom, 'prenom':prenom, 'temps': temps}

    return students_present


# Add Attendance of a specific user
def add_attendance(name, infos_seance):
    file_ids = []

    etudiant = Student.query.filter_by(id_etu=name).first()
    print(etudiant)
    if etudiant:
        id_etu = str(etudiant.id_etu)
        prenom = etudiant.prenom_etu
        nom = etudiant.nom_etu
        temps = datetime.now().strftime("%H:%M:%S")

    id_session = infos_seance['id_session']
    debut_session = infos_seance['seance_debut']
    attendance_dir = 'Attendance'
    attendance_file = os.path.join(attendance_dir, 'Session-{}-Date-{}.csv'.format(id_session, debut_session))

    if not os.path.isdir(attendance_dir):
        os.makedirs(attendance_dir)

    if attendance_file not in os.listdir(attendance_dir):
        with open(attendance_file, 'w') as f:
            f.write('ID_Etudiant,Nom,Prenom,Heure')

    # Clear file_ids list before reading the file
    file_ids = []

    with open(attendance_file, mode='r') as f:
        file_data = f.readlines()
        for row in file_data:
            file_ids.append(row.split(',')[0])

    if id_etu not in file_ids:
        with open(attendance_file, mode='a') as f:
            f.write(f'\n{id_etu},{nom},{prenom},{temps}')


################## ROUTING FUNCTIONS #########################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/professor')
def professor():
    elements_data = {}
    today_sessions = {}

    today_date = datetime.today()

    sessions = Seance.query.all()
    elements = Element.query.all()

    for element in elements:
        elements_data[element.id_elem] = element.nom_elem

    # Populate timetable_data dictionary
    max_sessions = 3
    session_count = 0

    for seance in sessions:
        session_id = seance.id_ses
        start_time = seance.debut_sess.strftime('%H:%M')
        end_time = seance.fin_sess.strftime('%H:%M')
        element_name = elements_data[seance.id_elem]


        if seance.date_ses.strftime("%Y-%m-%d") == today_date.strftime("%Y-%m-%d"):
            date = today_date.strftime("%b %d %Y")
            today_sessions[session_id] = {"id": session_id,"start": start_time, "end": end_time, "date": date, "element": element_name}
            session_count += 1
            if session_count >= max_sessions:
                break  # Stop adding sessions once the maximum limit is reached

    return render_template('professor.html', today_sessions=today_sessions)

@app.route('/absence', methods=['GET', 'POST'])
def absence():
    id_session = request.args.get('id_session')
    

    students_present = session.get('presence_{}'.format(id_session), {})

    seance = Seance.query.get(id_session)

    if seance:
        students = seance.etudiant_ses
        seance_debut = seance.debut_sess.strftime('%H-%M')

    session['seance_infos'] = {'id_session': id_session, 'seance_debut': seance_debut}
    return render_template('absence.html', students=students, id_session=id_session, students_present=students_present)

@app.route('/start', methods=['GET'])
def start():
    id_session = request.args.get('id_session')

    if 'students_present_{}'.format(id_session) not in session:
        session['students_present_{}'.format(id_session)] = {}

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
                    add_attendance(identified_person, {'id_session': id_session, 'seance_debut': session['seance_infos']['seance_debut']})
        cv.imshow('Attendance', frame)
        if cv.waitKey(1) == 27:
            break
    cap.release()
    cv.destroyAllWindows()
    
    students_present = extract_attendance({'id_session': id_session, 'seance_debut': session['seance_infos']['seance_debut']})
    session['presence_{}'.format(id_session)] = students_present
    return redirect(url_for('absence', id_session=id_session))


@app.route('/valider', methods=['POST', 'PUT', 'GET'])
def valider():
    id_session = request.args.get('id_session')
    students_present = request.form.getlist('present[]')

    # Check for missing entries in the received presence data
    for student_id in students_present:
        add_attendance(student_id, {'id_session': id_session, 'seance_debut': session['seance_infos']['seance_debut']})