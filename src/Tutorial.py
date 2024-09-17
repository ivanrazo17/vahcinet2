import customtkinter
from PIL import Image

def create_popup(parent, text, index, total, next_callback, prev_callback, finish_callback, position, gui_width):
    popup = customtkinter.CTkToplevel(parent)
    popup.title("Tutorial")
    popup.geometry("300x150")
    popup.grab_set()  # Make popup modal
    popup.overrideredirect(True)  # Remove window decorations
    poppins = customtkinter.CTkFont(family='Poppins', weight='normal', size=16)
    label = customtkinter.CTkLabel(popup, text=text, wraplength=250, font=poppins)
    label.pack(pady=10, padx=10, expand=True)  # Center the text with padding and expand

    button_frame = customtkinter.CTkFrame(popup)
    button_frame.pack(pady=10)

    if index > 0:
        prev_button = customtkinter.CTkButton(button_frame, text="Previous", command=prev_callback)
        prev_button.pack(side="left", padx=5)

    if index < total - 1:
        next_button = customtkinter.CTkButton(button_frame, text="Next", command=next_callback)
        next_button.pack(side="left", padx=5)
    elif text == "Finally, use the Music button to play music.":
        finish_button = customtkinter.CTkButton(button_frame, text="Finish", command=finish_callback)
        finish_button.pack(side="right", padx=5)

    # Position the popup to the right of the button
    popup.geometry(f"300x150+{position[0] + gui_width + 20}+{position[1]}")

    return popup

def show_tutorial(parent, button_frames, start_hide_timer):
    global tutorial_open  # Access the global variable

    tutorial_texts = [
        "Welcome to the VAHCINET! This is the Search button for locating local files.",
        "This is the Upload button. Use it to upload files to Google drive.",
        "Here is the LMS button for learning management system.",
        "Click on Files to access your files.",
        "Use the Browser button to open your web browser.",
        "This is the Eye Tracker button to control the mouse.",
        "Click on Voice Command to issue voice commands.",
        "Check the Command List button for available commands.",
        "Microsoft Tools button opens Microsoft tools.",
        "Finally, use the Music button to play music."
    ]

    index = 0
    popup = None

    def update_button_highlight(all_buttons=False):
        if all_buttons:
            # Set all buttons to #FCFCFA
            for button_frame in button_frames.values():
                for widget in button_frame.winfo_children():
                    if isinstance(widget, customtkinter.CTkButton):
                        widget.configure(fg_color="#FCFCFA")
        else:
            # Remove highlight from all buttons
            for button_frame in button_frames.values():
                for widget in button_frame.winfo_children():
                    if isinstance(widget, customtkinter.CTkButton):
                        widget.configure(fg_color="#FDFCFA")
            
            # Highlight the current button
            if button_frames:
                button_name = list(button_frames.keys())[index]
                button_frame = button_frames[button_name]
                for widget in button_frame.winfo_children():
                    if isinstance(widget, customtkinter.CTkButton):
                        widget.configure(fg_color="#FFFF00")

    def show_next():
        nonlocal index, popup
        if index < len(tutorial_texts) - 1:
            index += 1
            if popup:
                popup.destroy()
            button_name = list(button_frames.keys())[index]
            position = button_frames[button_name].winfo_rootx(), button_frames[button_name].winfo_rooty()
            popup = create_popup(
                parent,
                tutorial_texts[index],
                index,
                len(tutorial_texts),
                show_next,
                show_prev,
                finish_tutorial,
                position,
                parent.winfo_width()
            )
            update_button_highlight()  # Update highlight for the current button

    def show_prev():
        nonlocal index, popup
        if index > 0:
            index -= 1
            if popup:
                popup.destroy()
            button_name = list(button_frames.keys())[index]
            position = button_frames[button_name].winfo_rootx(), button_frames[button_name].winfo_rooty()
            popup = create_popup(
                parent,
                tutorial_texts[index],
                index,
                len(tutorial_texts),
                show_next,
                show_prev,
                finish_tutorial,
                position,
                parent.winfo_width()
            )
            update_button_highlight()  # Update highlight for the current button
   
    def finish_tutorial():
        nonlocal popup
        if popup:
            popup.destroy()
        global tutorial_open
        tutorial_open = False  # Set to False when tutorial is finished
        
        # Call update_button_highlight with all_buttons=True to reset all buttons' colors
        update_button_highlight(all_buttons=True)
        
        start_hide_timer()  # Start the hide timer after finishing the tutorial

    # Set tutorial_open to True when tutorial starts
    tutorial_open = True

    # Show the first popup
    button_name = list(button_frames.keys())[index]
    position = button_frames[button_name].winfo_rootx(), button_frames[button_name].winfo_rooty()
    popup = create_popup(
        parent,
        tutorial_texts[index],
        index,
        len(tutorial_texts),
        show_next,
        show_prev,
        finish_tutorial,
        position,
        parent.winfo_width()
    )
    update_button_highlight()  # Highlight the first button
