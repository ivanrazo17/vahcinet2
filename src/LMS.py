from PyQt5.QtGui import QDesktopServices, QGuiApplication
from PyQt5.QtCore import QUrl

def open_LMS():
    app = QGuiApplication.instance()
    if not app:
        app = QGuiApplication([])  # Create an application instance if it doesn't exist

    url = QUrl("https://cdm.blackboard.com/")
    QDesktopServices.openUrl(url)
