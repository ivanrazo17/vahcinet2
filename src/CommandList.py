import customtkinter
import json

# Define the paths for the tools JSON file
command_json_path = 'config/command_list.json'

def load_command_data():
    """ Load command data from JSON file """
    try:
        with open(command_json_path, 'r') as file:
            command_data = json.load(file)
        return command_data
    except FileNotFoundError:
        print(f"File not found: {command_json_path}")
        return {}

def add_commands_to_page(page, title, commands, title_font, command_font):
    """ Add a title and command labels to the page in two columns """
    # Add the title above the commands
    title_label = customtkinter.CTkLabel(master=page, text=title, font=title_font)
    title_label.pack(padx=20, pady=(10, 5), anchor="w")  # Adjusted padding

    # Add the commands below the title in two columns
    column_count = 2
    rows_per_column = (len(commands) + column_count - 1) // column_count  # Calculate rows per column

    frame = customtkinter.CTkFrame(master=page, fg_color="gray20", corner_radius=0)
    frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))  # Adjusted padding

    for idx, command in enumerate(commands):
        row = idx % rows_per_column
        col = idx // rows_per_column

        label = customtkinter.CTkLabel(master=frame, text=command, font=command_font, anchor="w")
        label.grid(row=row, column=col, padx=20, pady=5, sticky="ew")

    # Ensure that the columns stretch equally
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

def select_page(selected_page, all_pages):
    """ Select the current page to display """
    selected_page.pack(fill="both", expand=True)

    # Hide all other pages
    for page in all_pages:
        if page is not selected_page:
            page.pack_forget()

def open_CommandList():
    customtkinter.set_appearance_mode("dark")  # Ensure the dark theme is applied

    # Define the Segoe UI font styles
    segoe_ui_title_font = customtkinter.CTkFont(family='Segoe UI', weight='bold', size=16)
    segoe_ui_command_font = customtkinter.CTkFont(family='Segoe UI', weight='normal', size=14)

    """ Create a dark-themed popup window with command pages """
    # Create the main popup window
    popup = customtkinter.CTkToplevel()

    # Remove window decorations
    popup.overrideredirect(True)
    # Set the window attributes for a dark theme
    popup.configure(fg_color="gray10")  # Dark background
    popup.title("Command List")

    # Set the size and position of the popup window
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    popup_width = 650
    popup_height = 500

    x_position = (screen_width - popup_width) // 2
    y_position = (screen_height - popup_height) // 2
    popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

    # Create a custom title bar with only a close button
    title_bar = customtkinter.CTkFrame(master=popup, height=30, fg_color="gray20", corner_radius=0)
    title_bar.pack(fill="x", side="top")

    # Close button with no background and red hover effect
    close_button = customtkinter.CTkButton(master=title_bar, text="✕", command=popup.destroy, width=30, corner_radius=0,
                                          fg_color="transparent", hover_color="red")
    close_button.pack(side="right", padx=5, pady=5)

    # Create a frame to hold the pages and buttons
    content_frame = customtkinter.CTkFrame(master=popup, fg_color="gray10", corner_radius=0)
    content_frame.pack(fill="both", expand=True)

    # Create multiple pages (frames)
    page_1 = customtkinter.CTkFrame(master=content_frame, fg_color="gray20", corner_radius=0)
    page_2 = customtkinter.CTkFrame(master=content_frame, fg_color="gray20", corner_radius=0)
    page_3 = customtkinter.CTkFrame(master=content_frame, fg_color="gray20", corner_radius=0)

    # Save all pages in a list and add them to the content frame
    all_pages = [page_1, page_2, page_3]
    for page in all_pages:
        page.pack(fill="both", expand=True)

    # Load command data from JSON file
    command_data = load_command_data()

    # Titles for each page
    title_1 = "System Command & User Defined Command"
    title_2 = "System Command & Basic Application"
    title_3 = "System Command & Common Application"

    # Commands for each page
    commands_1 = command_data.get("System Command & User Defined Command", [])
    commands_2 = command_data.get("System Command & Basic Application", [])
    commands_3 = command_data.get("System Command & Common Application", [])

    # Add content to pages using the command data and titles
    add_commands_to_page(page_1, title_1, commands_1, segoe_ui_title_font, segoe_ui_command_font)
    add_commands_to_page(page_2, title_2, commands_2, segoe_ui_title_font, segoe_ui_command_font)
    add_commands_to_page(page_3, title_3, commands_3, segoe_ui_title_font, segoe_ui_command_font)

    # Create a frame for the buttons to center them
    button_frame = customtkinter.CTkFrame(master=content_frame, fg_color="gray10", corner_radius=0)
    button_frame.pack(fill="x", side="bottom", padx=10, pady=10)
    
    # Use grid layout to center buttons
    button_1 = customtkinter.CTkButton(master=button_frame, text="Page 1", command=lambda: select_page(page_1, all_pages))
    button_2 = customtkinter.CTkButton(master=button_frame, text="Page 2", command=lambda: select_page(page_2, all_pages))
    button_3 = customtkinter.CTkButton(master=button_frame, text="Page 3", command=lambda: select_page(page_3, all_pages))

    # Place buttons in grid layout
    button_1.grid(row=0, column=0, padx=5, pady=5)
    button_2.grid(row=0, column=1, padx=5, pady=5)
    button_3.grid(row=0, column=2, padx=5, pady=5)

    # Adjust column weights to center buttons
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

    # Select initial page
    select_page(page_1, all_pages)

    # Start the main loop for the popup
    popup.mainloop()
