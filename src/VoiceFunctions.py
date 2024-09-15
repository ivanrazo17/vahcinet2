# VoiceFunctions.py
import os
import json
import numpy as np
import tempfile
import subprocess
import webbrowser
import pyautogui
import re
import platform
from typing import Callable

def extract_features(myrecording: np.ndarray, fs: int, expected_features: int = 64000) -> np.ndarray:
    window_size = 5000  # milliseconds
    n_frames = int(window_size * fs / 1000)
    
    # Convert to a NumPy array if it's not already
    myrecording = np.asarray(myrecording)
    
    # Trim or pad the recording to exactly `expected_features` samples
    if len(myrecording) > expected_features:
        myrecording = myrecording[:expected_features]
    elif len(myrecording) < expected_features:
        myrecording = np.pad(myrecording, (0, expected_features - len(myrecording)))
    
    # Flatten the array
    raw_features = myrecording.flatten()
    
    return raw_features

def write_to_json_file(features: np.ndarray, filename: str = 'input.json') -> None:
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, 'data', 'input')    
    file_path = os.path.join(directory_path, filename)

    # Write features to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump({'features': features.tolist()}, json_file)  # Convert numpy array to list before saving as JSON

def clear_json_file(filename: str = 'data/input/voice_command_data.json') -> None:
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, filename)

    # Clear the JSON contents by writing an empty JSON object
    with open(file_path, 'w') as file:
        json.dump({}, file)

def classify_features(raw_features: np.ndarray, update_gui: Callable[[str], None]) -> str:
    # Write features to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
        temp.write(','.join(map(str, raw_features)))
        temp_path = temp.name
    
    current_directory = os.getcwd()
    js_script_path = os.path.join(current_directory, 'model', 'run-impulse.js')

    try:
        # Call Node.js process and pass the temporary filename
        result = subprocess.check_output(['node', js_script_path, temp_path])
        result = result.decode('utf-8').strip()

        # Filter out the specific message and unwanted fields
        lines = result.split('\n')
        filtered_result_lines = [
            line for line in lines
            if "Running inference for Colegio De Muntinlupa" not in line and
               not any(field in line for field in ['anomaly:', 'visual_ad_max:', 'visual_ad_mean:'])
        ]
        
        filtered_result = '\n'.join(filtered_result_lines)
        
        if filtered_result:
            # Save only the filtered result to JSON file
            processed_file_path = os.path.join(current_directory, 'data', 'processed', 'processed_data.json')
            os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
            with open(processed_file_path, 'w') as file:
                json.dump({'result': filtered_result}, file, indent=4)
            
            return filtered_result
        else:
            return "No valid results from classification."

    except subprocess.CalledProcessError as e:
        update_gui(f"Failed to initialize classifier. Error: {e}")
        return "Classification failed."

def get_search_query_from_json(filename: str = 'data/input/speech_text.json') -> str:
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, filename)

    # Read the search query from the JSON file
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            recognized_text = data.get('recognized_text', '').strip()
            
            # Extract the search query based on known patterns
            if recognized_text.startswith('open browser and search ') or recognized_text.startswith('open google and search ') or recognized_text.startswith('open youtube and search '):
                query = recognized_text.split('search ', 1)[-1].strip()
                return query
            else:
                return ''
    else:
        return ''

def open_youtube_and_search(update_gui: Callable[[str], None]) -> None:
    query = get_search_query_from_json()
    if query:
        search_url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(search_url)
        update_gui(f"Opened YouTube and searched for '{query}'.")
    else:
        update_gui("No search query provided.")

def open_browser_and_search(update_gui: Callable[[str], None]) -> None:
    query = get_search_query_from_json()
    if query:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        update_gui(f"Opened browser and searched for '{query}'.")
    else:
        update_gui("No search query provided.")

def open_google_and_search(update_gui: Callable[[str], None]) -> None:
    query = get_search_query_from_json()
    if query:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        update_gui(f"Opened google and searched for '{query}'.")
    else:
        update_gui("No search query provided.")

def perform_print(update_gui: Callable[[str], None]) -> None:
    pyautogui.hotkey('ctrl', 'p')
    update_gui("Ctrl+P simulated for printing")

def perform_save(update_gui: Callable[[str], None]) -> None:
    pyautogui.hotkey('ctrl', 's')
    update_gui("Ctrl+S simulated for saving")

def close_google_tab(update_gui: Callable[[str], None]) -> None:
    if platform.system() == "Windows" or platform.system() == "Linux":
        pyautogui.hotkey('ctrl', 'w')  # Close current tab (Ctrl + W)
    elif platform.system() == "Darwin":  # macOS
        pyautogui.hotkey('command', 'w')  # Close current tab (Cmd + W)
    update_gui("Active browser tab closed.")

def output_prediction(config_filename: str = 'config/config.json', data_filename: str = 'data/processed/processed_data.json', update_gui: Callable[[str], None] = None) -> None:
    current_directory = os.getcwd()
    config_path = os.path.join(current_directory, config_filename)
    data_path = os.path.join(current_directory, data_filename)

    def handle_print():
        perform_print(update_gui)

    def handle_save_file():
        perform_save(update_gui)

    def handle_open_google_and_search():
        open_google_and_search(update_gui)

    def handle_exit_google():
        close_google_tab(update_gui)

    def handle_open_youtube_and_search():
        open_youtube_and_search(update_gui)

    def handle_open_browser_and_search():
        open_browser_and_search(update_gui)

    def handle_default(max_label: str):
        
        if max_label.startswith("Open"):
            subprocess.Popen(actions[max_label], shell=True)
            update_gui(f"You {max_label}.")
        elif (max_label == "Noise"):
            update_gui(f"{max_label} was detected.")
        else:
            app_name = actions[max_label]
            result = subprocess.run(["taskkill", "/IM", app_name, "/F"], capture_output=True, text=True)
            if result.returncode == 0:
                update_gui(f"You {max_label}.")
            else:
                update_gui(f"Failed to Execute {max_label} app: {result.stderr}")

    try:
        # Load actions from JSON config file
        with open(config_path, 'r') as config_file:
            actions = json.load(config_file)

        # Load data from JSON data file
        with open(data_path, 'r') as data_file:
            content = data_file.read()
            labels_and_values = re.findall(r"label: '([^']*)', value: ([\d.]+)", content)
            
            if labels_and_values:
                max_label, max_value = max(labels_and_values, key=lambda x: float(x[1]))
                # Define the dispatch table
                switch_case = {
                    "Print": handle_print,
                    "Save File": handle_save_file,
                    "Open google and search": handle_open_google_and_search,
                    "Exit Google": handle_exit_google,
                    "Open youtube and search": handle_open_youtube_and_search,
                    "Open Browser and search": handle_open_browser_and_search,
                }

                # Call the corresponding function based on the label
                handler = switch_case.get(max_label, lambda: handle_default(max_label))
                handler()

            else:
                update_gui("No labels and values found in the data file.")

    except FileNotFoundError as e:
        update_gui(f"Error: {e.filename} not found.")
    except json.JSONDecodeError:
        update_gui("Error: Failed to decode JSON from the configuration file.")
    except Exception as e:
        update_gui(f"An unexpected error occurred: {e}")
