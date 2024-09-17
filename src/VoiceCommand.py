# VoiceCommand.py
import os
import time
import wave
import json
import numpy as np
import pyaudio
import speech_recognition as sr
import customtkinter as ctk
from .VoiceFunctions import extract_features, write_to_json_file, clear_json_file, classify_features, output_prediction


ctk.set_appearance_mode('dark')

# Function to update GUI with messages
def update_gui(message: str):
    if app:  # Ensure app is initialized
        app.output_label.configure(text=message)
        app.update()  # Force the GUI to update immediately

def record_audio(duration, fs, filename='recording.wav', sample_rate=16000):
    # Countdown before recording
    countdown_time = 3
    while countdown_time > 0:
        update_gui(f"Starting recording in {countdown_time} seconds...")
        time.sleep(1)
        countdown_time -= 1

    update_gui(f"Recording audio for {duration} seconds...")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=fs,
                    input=True,
                    frames_per_buffer=int(fs/10))  # Adjust frames_per_buffer as needed

    frames = []

    for i in range(0, int(fs / int(fs/10) * duration)):
        data = stream.read(int(fs/10))
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

    # Ensure the data/input folder exists
    os.makedirs('data/input', exist_ok=True)
    
    # Path for the audio file
    audio_file_path = os.path.join('data/input', filename)
    
    # Save the audio data to a WAV file
    with wave.open(audio_file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    # Convert audio to text using SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)        
        # Save the recognized text to speech_text.json
        text_file_path = os.path.join('data/input', 'speech_text.json')
        with open(text_file_path, 'w') as json_file:
            json.dump({'recognized_text': text}, json_file)
            
    except sr.UnknownValueError:
        text = "Error: Could not understand audio due to noise"
        # Save error message to JSON
        text_file_path = os.path.join('data/input', 'speech_text.json')
        with open(text_file_path, 'w') as json_file:
            json.dump({'recognized_text': text}, json_file)
    except sr.RequestError as e:
        print(f"Could not request results from Recognition service; {e}")
        text = f"Error: {e}"
        # Save error message to JSON
        text_file_path = os.path.join('data/input', 'speech_text.json')
        with open(text_file_path, 'w') as json_file:
            json.dump({'recognized_text': text}, json_file)

    # Delete the audio file
    os.remove(audio_file_path)

    return audio_data

# Main Function
def run_voice_command():
    global app
    app = ctk.CTk()  # Create the CTk main window
    app.title("Voice Command App")
    app = ctk.CTkToplevel()
    # Make the window stay on top of all other windows
    app.attributes('-topmost', 1)

    screen_width = app.winfo_screenwidth()

    app_width = 340 # Increased width to fit more buttons
    app_height = 70  # Increased height to fit text and icons
    x = (screen_width // 2) - (app_width // 2)
    y = 0  # Position at the top
    app.geometry(f"{app_width}x{app_height}+{x}+{y}")
    # Remove window decorations
    app.overrideredirect(True)

    # Create and place labels and buttons
    app.output_label = ctk.CTkLabel(app, wraplength=400)
    app.output_label.pack(pady=20, padx=20)

    # Model Parameters
    duration = 5 
    fs = 16000
    expected_features = 64000 

    # Record audio
    myrecording = record_audio(duration, fs)

    # Calculate the number of extracted features
    raw_features = extract_features(myrecording, fs, expected_features)

    # Use the new function to write features to a JSON file
    write_to_json_file(raw_features, filename='voice_command_data.json')

    try:
        classify_features(raw_features, update_gui)
    except Exception as e:
        print(f"Exception during classification: {e}")
    finally:
        # Clear contents of features.txt after program exits
        clear_json_file(filename='data/input/voice_command_data.json')
        # Show output
        output_prediction(config_filename='config/config.json', data_filename='data/processed/processed_data.json', update_gui=update_gui)
    



