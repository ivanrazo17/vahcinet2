import customtkinter
import ctypes
from PIL import Image
import json
import time

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')
customtkinter.set_appearance_mode('dark')
app = customtkinter.CTk()
maxHeight = app.winfo_screenheight()
maxWidth = 200

# Store the original position
original_x, original_y = -9, 0
app_visible = True  # To track if the app is visible or hidden
hide_timer = None  # Timer reference for hiding the app

app.attributes('-alpha', 0.9)
app.geometry(f'{maxWidth}x{maxHeight}+{original_x}+{original_y}')
app.title('VAHCINET')
app.iconbitmap("assets/VahcinetIcon.ico")

# Make the window stay on top of all other windows
app.attributes('-topmost', 1)

# Define constants for Windows window styles
GWL_STYLE = -16
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_THICKFRAME = 0x00040000

# Function to remove minimize, maximize, and resize buttons
def remove_window_borders(window):
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~WS_MINIMIZEBOX
    style &= ~WS_MAXIMIZEBOX
    style &= ~WS_THICKFRAME
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)

# Function to load button data from JSON file
def load_button_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Load button data
button_data = load_button_data('config/button_data.json')

# Function to create buttons with icons (image on top, text at the bottom)
def create_buttons(container, button_info):
    poppins = customtkinter.CTkFont(family='Poppins', weight='normal', size=16)
    
    for name, icon_path in button_info.items():
        button_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        button_frame.pack(padx=5, pady=5, fill='x')
        
        image = Image.open(icon_path)
        ctk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(45, 45))
        
        button = customtkinter.CTkButton(
            button_frame,
            image=ctk_image,
            text="",
            fg_color="#FDFCFA",
            hover_color="#F6F6F6",
            corner_radius=50,
            width=45,
            height=45,
            cursor="hand2"
        )
        button.pack()
        
        text_label = customtkinter.CTkLabel(
            button_frame,
            text=name,
            text_color="#FFFFFF",
            font=poppins
        )
        text_label.pack()

def hide_app():
    global app_visible
    if app_visible:
        for i in range(0, maxWidth + 1, 5):
            app.geometry(f'{maxWidth}x{maxHeight}+-{i}+0')
            app.update_idletasks()
            time.sleep(0.01)
        app_visible = False

def restore_position():
    global app_visible
    if not app_visible:
        for i in range(maxWidth, -original_x, -5):
            app.geometry(f'{maxWidth}x{maxHeight}+{-i}+{original_y}')
            app.update_idletasks()
            time.sleep(0.01)
        app.geometry(f'{maxWidth}x{maxHeight}+{original_x}+{original_y}')
        app_visible = True
        
def is_cursor_within_geometry():
    cursor_x = app.winfo_pointerx()
    cursor_y = app.winfo_pointery()
    app_x = app.winfo_rootx()
    app_y = app.winfo_rooty()
    if app_x <= cursor_x <= app_x + maxWidth and app_y <= cursor_y <= app_y + maxHeight:
        return True
    return False

def start_hide_timer():
    global hide_timer
    if hide_timer:
        app.after_cancel(hide_timer)
    # Start the timer only if the cursor is not within the app's geometry
    if not is_cursor_within_geometry():
        hide_timer = app.after(2000, hide_app)

def on_mouse_enter(event):
    restore_position()
    start_hide_timer()

def on_mouse_leave(event):
    start_hide_timer()

app.bind("<Enter>", on_mouse_enter)
app.bind("<Leave>", on_mouse_leave)

button_container = customtkinter.CTkFrame(app, width=100, fg_color="transparent")
button_container.pack(side='top', fill='y', padx=10, pady=10)

app.after(10, lambda: remove_window_borders(app))
app.after(20, lambda: create_buttons(button_container, button_data))

start_hide_timer()

app.mainloop()
