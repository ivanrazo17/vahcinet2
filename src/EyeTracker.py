import sys
import cv2
import pyautogui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import mediapipe as mp

def run_eye_tracker():
    # Ensure a QApplication object is created
    app = QApplication(sys.argv)
    
    popup = QDialog()
    popup.setWindowTitle("ET Mouse")

    # Manually set position for popup (adjust the values as necessary)
    widget_pos_x = 35
    widget_pos_y = 0
    popup.setGeometry(widget_pos_x + 150, widget_pos_y, 150, 160)

    popup.setStyleSheet("background-color: black; color: white;")
    popup.setWindowOpacity(0.8)
    popup.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    popup_layout = QVBoxLayout(popup)

    # Close button
    close_button = QPushButton("X", popup)
    close_button.setStyleSheet("background-color: red; color: white; border: none;")
    close_button.clicked.connect(popup.reject)
    close_button.setMinimumSize(20, 20)

    popup_layout.addWidget(close_button, alignment=Qt.AlignTop | Qt.AlignRight)

    # Buttons for camera selection
    button_integrated = QPushButton("Integrated Cam", popup)
    button_integrated.setMinimumSize(50, 50)
    button_integrated.setStyleSheet(
            "border: 1px solid white; background-color: Black; color: white; font-weight: bold; font-size: 15px;")

    button_dedicated = QPushButton("Webcam", popup)
    button_dedicated.setMinimumSize(30, 50)
    button_dedicated.setStyleSheet(
            "border: 1px solid white; background-color: Black; color: white; font-weight: bold; font-size: 20px;")

    button_integrated.clicked.connect(integrated_function)
    button_dedicated.clicked.connect(dedicated_function)

    popup_layout.addWidget(button_integrated)
    popup_layout.addWidget(button_dedicated)

    popup.exec_()
    
    # Start the application's event loop
    sys.exit(app.exec_())

def integrated_function():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)

        rbg_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rbg_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    pyautogui.moveTo(screen_x, screen_y)

            left = [landmarks[145], landmarks[159]]
            right = [landmarks[374], landmarks[386]]

            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

            for landmark in right:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (255, 0, 0))

            if (left[0].y - left[1].y) < 0.002:
                pyautogui.click(button='left')
            if (right[0].y - right[1].y) < 0.003:
                pyautogui.click(button='right')

        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1)

def dedicated_function():
    cam = cv2.VideoCapture(1)  # Webcam (dedicated cam)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)  # Flip horizontally only, to match a mirror image effect

        rbg_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rbg_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    pyautogui.moveTo(screen_x, screen_y)

            left = [landmarks[145], landmarks[159]]
            right = [landmarks[374], landmarks[386]]

            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

            for landmark in right:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (255, 0, 0))

            # Blink detection for clicks
            if (left[0].y - left[1].y) < 0.002:
                pyautogui.click(button='left')
            if (right[0].y - right[1].y) < 0.003:
                pyautogui.click(button='right')

        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1)

