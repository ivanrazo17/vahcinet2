from PyQt5.QtGui import QDesktopServices, QGuiApplication
from PyQt5.QtCore import QUrl

def open_Browser():
    app = QGuiApplication.instance()
    if not app:
        app = QGuiApplication([])  # Create an application instance if it doesn't exist

    url = QUrl("https://www.google.com/")
    QDesktopServices.openUrl(url)