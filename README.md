# FacePresence: Effortless Attendance, Powered by Your Face

------------------------------------------------------------

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation Guide](#installation-guide)
5. [Usage](#usage)
6. [System Architecture](#system-architecture)
7. [Challenges](#challenges)
8. [Future Enhancements](#future-enhancements)
9. [Contributors](#contributors)
10. [License](#license)

------------------------------------------------------------

## Project Overview
FacePresence is an innovative web application that automates attendance management using facial recognition technology. It offers an efficient, intuitive, and AI-powered solution for schools or organizations.  

This application leverages YOLOv8 for face detection and an SVM model for face recognition to create a seamless, real-time attendance system. The project aims to modernize and simplify attendance workflows while ensuring high accuracy and reliability.

------------------------------------------------------------

## Features
- **User Authentication**: Secure login system for administrators and professors.
- **Real-Time Attendance Management**: Facial recognition for automatic marking of attendance.
- **Absence Justifications**: Enables students to submit absence justifications directly through the platform.
- **Reporting Tools**: Attendance and absence records can be exported as reports.
- **Responsive Web Interface**: Fully optimized for use on all device sizes.

------------------------------------------------------------

## Technologies Used
- **Frontend**: 
  - HTML, CSS, JavaScript
  - Responsive design with Bootstrap
- **Backend**: 
  - Python (Flask)
- **Database**: 
  - SQLite for lightweight and efficient data storage
- **AI Models**: 
  - YOLOv8 for face detection
  - SVM (Support Vector Machine) for face recognition
- **Libraries**: 
  - OpenCV
  - PyTorch
  - Flask-SQLAlchemy

------------------------------------------------------------

## Installation Guide
Follow these steps to set up and run the project locally:

1. **Clone the repository**:
    git clone https://github.com/Nizar-Bahajoub/Alx-Webstack-Protfolio.git
2. **Navigate to the project directory**:
        cd FacePresence

3. **Set up a virtual environment**:
        python -m venv venv
        source venv/bin/activate   # For Linux/Mac
        venv\Scripts\activate      # For Windows

4. **Install the required dependencies**:
        pip install -r requirements.txt

5. **Set up the database**:
        python create_db.py

6. **Run the application**:
        python run.py

7. **ccess the web application**:
    Open your browser and go to http://localhost:5000.

------------------------------------------------------------

## Usage

### Steps to Use the System:
1. **Register Users**: Upload facial images to register users in the system.  
2. **Mark Attendance**: Users' attendance is automatically recorded when they are detected via the facial recognition system.  
3. **Manage Absences**: Professors and administrators can manage absence justifications through the admin panel.  

### Directory Structure:
- `app_pack/`: Core application logic, including routing and templates.  
- `dbModels/`: Database models for managing user data.  
- `models/`: Pre-trained AI models (YOLOv8, SVM).  
- `static/`: Static files such as CSS, JavaScript, and images.  
- `templates/`: HTML templates for the frontend.  

------------------------------------------------------------

## System Architecture
### Frontend:
The user interface is built using HTML, CSS, and JavaScript, designed to be responsive and user-friendly.

### Backend:
Powered by Flask, the backend handles requests, routes, and database queries.

### AI Models:
- **YOLOv8**: Detects faces in images or video streams.  
- **SVM**: Classifies and matches detected faces with registered users for attendance tracking.  

### Database:
MySQL is used to store user profiles, attendance records, and system configurations.

------------------------------------------------------------

## Challenges
- **Real-Time Performance**: Ensuring the system can handle real-time recognition without noticeable delays.  
- **Model Accuracy**: Fine-tuning AI models to achieve high precision in various lighting and environmental conditions.  
- **Data Storage**: Managing and scaling the database for large user bases.  

------------------------------------------------------------

## Future Enhancements
1. **Cloud Deployment**: Host the system on a cloud platform for scalability.  
2. **Multi-Language Support**: Add support for additional languages to accommodate a global user base.  
3. **Role-Based Access Control**: Implement different levels of access for students, professors, and administrators.  
4. **Mobile App**: Develop a mobile application for improved accessibility.  

---

## Contributors
- **Nizar Bahajoub**

Feel free to contribute by submitting a pull request or opening an issue.

