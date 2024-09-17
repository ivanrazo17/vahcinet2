import tkinter as tk
import customtkinter as ctk
import subprocess
import json
from PIL import Image

# Define the paths for the tools JSON file
tools_json_path = 'config/tools_icon.json'

def open_MsOfficePopup():
    popup = ctk.CTkToplevel()
    # Make the window stay on top of all other windows
    popup.attributes('-topmost', 1)
    # Remove window decorations
    popup.overrideredirect(True)

    # Center the popup at the top middle of the screen
    screen_width = popup.winfo_screenwidth()
    popup_width = 1150  # Increased width to fit more buttons
    popup_height = 100  # Increased height to fit text and icons
    x = (screen_width // 2) - (popup_width // 2)
    y = 0  # Position at the top
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    # Define application commands directly in the function
    commands = {
        "Office": ["start", "winword.exe"],
        "PowerPoint": ["start", "powerpnt.exe"],
        "Excel": ["start", "excel.exe"],
        "Outlook": ["start", "outlook.exe"],
        "OneNote": ["start", "onenote.exe"],
        "Publisher": ["start", "publisher.exe"],
        "Teams": [r"%LOCALAPPDATA%\Microsoft\Teams\current\Teams.exe"],  # Updated path for Teams
        "Zoom": [r"%APPDATA%\Zoom\bin\Zoom.exe"],  # Updated path for Zoom
    }

    # Create a frame to hold the buttons
    button_frame = ctk.CTkFrame(popup, fg_color='#EBEBEB')
    button_frame.pack(expand=True, fill='both', padx=10, pady=10)

    # Load button data from JSON
    with open(tools_json_path, 'r') as file:
        button_data = json.load(file)

    # Create buttons dynamically based on the JSON data
    for name, details in button_data.items():
        icon_path = details["icon"]
        function = commands.get(name, None)

        # Frame for each button
        button_frame_inner = ctk.CTkFrame(button_frame, fg_color='#EBEBEB')
        button_frame_inner.pack(side='left', padx=10, pady=10, fill='both')

        # Load and set image
        image = Image.open(icon_path)
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(45, 45))

        # Create button
        button = ctk.CTkButton(
            button_frame_inner,
            image=ctk_image,
            text=name,  # Set the text for the button
            text_color="#000000",  # Set text color to black for better visibility
            fg_color="#EBEBEB",
            hover_color="#D3D3D3",
            corner_radius=10,
            width=75,  # Adjust width to fit text and icon
            height=75,  # Adjust height to fit text and icon
            cursor="hand2",
            command=lambda cmd=function: [subprocess.Popen(cmd, shell=True), popup.destroy()] if cmd else None
        )
        button.pack(pady=5)  # Add padding around the button

    popup.mainloop()
