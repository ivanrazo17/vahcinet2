from src import function_map
from src.Tutorial import show_tutorial  # Import the function from Tutorial.py
import customtkinter
import ctypes
import json
import time
import threading
from PIL import Image
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to load the tutorial flag from config/flag.json
def load_tutorial_flag(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to save the tutorial flag after it has been shown
def save_tutorial_flag(filename, flag_data):
    with open(filename, 'w') as file:
        json.dump(flag_data, file, indent=4)

# Load the tutorial flag
flag_file = resource_path('config\\flag.json')
tutorial_flag = load_tutorial_flag(flag_file)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')
customtkinter.set_appearance_mode('dark')
app = customtkinter.CTk()
maxHeight = app.winfo_screenheight()
maxWidth = 200

# Store the original position
original_x, original_y = -9, 0
app_visible = True  # To track if the app is visible or hidden
hide_timer = None  # Timer reference for hiding the app
tutorial_open = False  # To track if the tutorial is open

app.attributes('-alpha', 0.9)
app.geometry(f'{maxWidth}x{maxHeight}+{original_x}+{original_y}')
app.title('VAHCINET')
app.iconbitmap(resource_path("favicon.ico"))

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
button_data = load_button_data(resource_path('config\\button_data.json'))

# Function to scale UI elements based on screen resolution
def scale_value(base_value, scaling_factor):
    return int(base_value * scaling_factor)

# Get the current screen resolution
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Define the base resolution (1080p)
base_width = 1920
base_height = 1080

# Calculate scaling factors based on the current resolution
width_scaling = screen_width / base_width
height_scaling = screen_height / base_height

# Apply scaling to the GUI and button sizes
scaled_button_size = scale_value(45, min(width_scaling, height_scaling))  # Uniform scaling for buttons
scaled_frame_padding = scale_value(5, min(width_scaling, height_scaling))

# Function to create buttons with icons (image on top, text at the bottom)
def create_button(button_frame, name, icon_path, function, highlight=False):
    image = Image.open(icon_path)
    # Adjust the image size based on scaling
    ctk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(scaled_button_size, scaled_button_size))
    
    poppins = customtkinter.CTkFont(family='Poppins', weight='normal', size=scale_value(16, height_scaling))

    border_color = "#FFFF00" if highlight else "#FDFCFA"

    button = customtkinter.CTkButton(
        button_frame,
        image=ctk_image,
        text="",
        fg_color=border_color,
        hover_color="#D3D3D3",
        corner_radius=scale_value(50, height_scaling),
        width=scaled_button_size,
        height=scaled_button_size,
        cursor="hand2",
        command=lambda: threading.Thread(target=function).start()
    )
    button.pack()

    text_label = customtkinter.CTkLabel(
        button_frame,
        text=name,
        text_color="#FFFFFF",
        font=poppins
    )
    text_label.pack()

def create_buttons(container, button_info):
    button_frames = {} 
    stop_at_button_name = "Music"

    for name, details in button_info.items():
        if name == stop_at_button_name:
            icon_path = details["icon"]
            function_name = details["function"]
            function = function_map.get(function_name, None)

            button_frame = customtkinter.CTkFrame(container, fg_color="transparent")
            button_frame.pack(padx=scaled_frame_padding, pady=scaled_frame_padding, fill='x')

            create_button(button_frame, name, icon_path, function)
            button_frames[name] = button_frame
            break  

        icon_path = details["icon"]
        function_name = details["function"]
        function = function_map.get(function_name, None)

        button_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        button_frame.pack(padx=scaled_frame_padding, pady=scaled_frame_padding, fill='x')

        create_button(button_frame, name, icon_path, function)
        button_frames[name] = button_frame

    return button_frames

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
    if not is_cursor_within_geometry() and not tutorial_open:
        hide_timer = app.after(2000, hide_app)

def on_mouse_enter(event):
    restore_position()
    start_hide_timer()

def on_mouse_leave(event):
    start_hide_timer()

# Create the button frame and buttons
button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
button_frame.pack(fill="both", expand=True)

button_frames = create_buttons(button_frame, button_data)

app.bind("<Enter>", on_mouse_enter)
app.bind("<Leave>", on_mouse_leave)

# Run the tutorial only if the flag is False
if not tutorial_flag.get("tutorial_shown", False):
    show_tutorial(app, button_frames, start_hide_timer)
    tutorial_flag["tutorial_shown"] = True
    save_tutorial_flag(flag_file, tutorial_flag) 

app.after(10, lambda: remove_window_borders(app))
app.mainloop()
