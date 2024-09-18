import customtkinter
from PIL import Image

# Function to scale UI elements based on screen resolution
def scale_value(base_value, scaling_factor):
    return int(base_value * scaling_factor)

# Popup creation function with screen resolution scaling and boundary check
def create_popup(parent, text, index, total, next_callback, prev_callback, finish_callback, position, gui_width, scaling_factors):
    popup = customtkinter.CTkToplevel(parent)
    popup.title("Tutorial")

    # Get screen resolution
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Apply scaling to popup dimensions
    popup_width = scale_value(300, scaling_factors["width"])
    popup_height = scale_value(150, scaling_factors["height"])
    popup.geometry(f"{popup_width}x{popup_height}")
    popup.grab_set()  # Make popup modal
    popup.overrideredirect(True)  # Remove window decorations

    # Scale font size
    poppins_font_size = scale_value(16, scaling_factors["height"])
    poppins = customtkinter.CTkFont(family='Poppins', weight='normal', size=poppins_font_size)

    # Scale label padding and wraplength
    label_wraplength = scale_value(250, scaling_factors["width"])
    label_padding = scale_value(10, scaling_factors["width"])

    label = customtkinter.CTkLabel(popup, text=text, wraplength=label_wraplength, font=poppins)
    label.pack(pady=label_padding, padx=label_padding, expand=True)

    # Button frame and buttons
    button_frame = customtkinter.CTkFrame(popup)
    button_frame.pack(pady=label_padding)

    # Button size scaling
    button_width = scale_value(90, scaling_factors["width"])  # Set consistent button width
    button_height = scale_value(30, scaling_factors["height"])  # Scaled button height

    if index > 0:
        prev_button = customtkinter.CTkButton(
            button_frame, 
            text="Previous", 
            command=prev_callback,
            width=button_width,  # Set scaled width
            height=button_height  # Set scaled height
        )
        prev_button.pack(side="left", padx=scale_value(5, scaling_factors["width"]))

    if index < total - 1:
        next_button = customtkinter.CTkButton(
            button_frame, 
            text="Next", 
            command=next_callback,
            width=button_width,  # Set same width for next button
            height=button_height  # Set scaled height
        )
        next_button.pack(side="left", padx=scale_value(5, scaling_factors["width"]))
    elif text == "Finally, use the Music button to play music.":
        finish_button = customtkinter.CTkButton(
            button_frame, 
            text="Finish", 
            command=finish_callback,
            width=button_width,  # Set same width for finish button
            height=button_height  # Set scaled height
        )
        finish_button.pack(side="right", padx=scale_value(5, scaling_factors["width"]))

    # Position the popup next to the button, considering scaling
    popup_x = position[0] + gui_width + scale_value(20, scaling_factors['width'])
    popup_y = position[1]

    # Ensure the popup does not overflow the screen's right or bottom edges
    if popup_x + popup_width > screen_width:
        popup_x = screen_width - popup_width - scale_value(20, scaling_factors['width'])
    if popup_y + popup_height > screen_height:
        popup_y = screen_height - popup_height - scale_value(20, scaling_factors['height'])

    # Ensure popup doesn't go out of bounds at the top or left side
    popup_x = max(popup_x, 0)
    popup_y = max(popup_y, 0)

    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

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

    # Define scaling factors based on the screen resolution
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    base_width = 1920
    base_height = 1080
    width_scaling = screen_width / base_width
    height_scaling = screen_height / base_height
    scaling_factors = {"width": width_scaling, "height": height_scaling}

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
                parent.winfo_width(),
                scaling_factors  # Pass scaling factors to popup creation
            )
            popup.attributes('-topmost', 1)  # Keep the popup on top
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
                parent.winfo_width(),
                scaling_factors  # Pass scaling factors to popup creation
            )
            popup.attributes('-topmost', 1)  # Keep the popup on top
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
        parent.winfo_width(),
        scaling_factors  # Pass scaling factors to popup creation
    )
    popup.attributes('-topmost', 1)  # Keep the first popup on top
    update_button_highlight()  # Highlight the first button
