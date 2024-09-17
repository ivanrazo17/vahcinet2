import sys
import cv2
import pyautogui
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import mediapipe as mp

def run_eye_tracker():
    app = QApplication(sys.argv)
    window = QDialog()
    window.setWindowTitle("ET Mouse")

    # Get screen dimensions
    screen_rect = QApplication.primaryScreen().geometry()
    screen_width = screen_rect.width()
    screen_height = screen_rect.height()

    # Set window size
    window_width = 500
    window_height = 400

    # Calculate position to place window on the right side and center it vertically
    x = screen_width - window_width - 30  # 50 pixels from the right edge
    y = (screen_height - window_height) // 2

    window.setGeometry(x, y, window_width, window_height)

    window.setStyleSheet("background-color: black; color: white;")
    window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    layout = QVBoxLayout(window)

    # Close button
    close_button = QPushButton("✕", window)
    close_button.setStyleSheet("background-color: red; color: white; border: none;")
    close_button.clicked.connect(window.reject)
    close_button.setMinimumSize(40, 40)
    close_button.setCursor(Qt.PointingHandCursor)  # Set cursor directly
    layout.addWidget(close_button, alignment=Qt.AlignTop | Qt.AlignRight)

    # Video display
    video_label = QLabel(window)
    video_label.setFixedSize(500, 300)  # Made the video frame smaller
    layout.addWidget(video_label)

    # Buttons for camera selection
    button_layout = QHBoxLayout()
    layout.addLayout(button_layout)

    button_integrated = QPushButton("Integrated Cam", window)
    button_integrated.setMinimumSize(150, 50)
    button_integrated.setStyleSheet(
        "border: 1px solid white; background-color: Black; color: white; font-weight: bold; font-size: 15px;")
    button_integrated.setCursor(Qt.PointingHandCursor)  # Set cursor directly
    button_layout.addWidget(button_integrated)

    button_dedicated = QPushButton("Webcam", window)
    button_dedicated.setMinimumSize(150, 50)
    button_dedicated.setStyleSheet(
        "border: 1px solid white; background-color: Black; color: white; font-weight: bold; font-size: 15px;")
    button_dedicated.setCursor(Qt.PointingHandCursor)  # Set cursor directly
    button_layout.addWidget(button_dedicated)

    # Camera control functions
    def start_camera(cam_index):
        global cam
        cam = cv2.VideoCapture(cam_index)
        global face_mesh
        face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        global timer
        timer = QTimer()
        timer.timeout.connect(lambda: update_frame(video_label))
        timer.start(30)

    def start_integrated_cam():
        start_camera(0)

    def start_dedicated_cam():
        start_camera(1)

    button_integrated.clicked.connect(start_integrated_cam)
    button_dedicated.clicked.connect(start_dedicated_cam)

    def update_frame(video_label):
        global cam
        global face_mesh

        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = pyautogui.size().width / frame_w * x
                    screen_y = pyautogui.size().height / frame_h * y
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

        # Convert frame to QImage
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Update QLabel with QImage
        pixmap = QPixmap.fromImage(q_image)
        video_label.setPixmap(pixmap)

    window.exec_()

