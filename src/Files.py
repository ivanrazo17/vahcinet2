import threading
import pyautogui

def open_Files():
    pyautogui.hotkey("winleft", "e")
    pyautogui.hotkey("ctrl", "e")

search_thread = threading.Thread(target=open_Files)
