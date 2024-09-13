import subprocess
import os
def open_Music():
    # Path to MediaPlayer.exe in the AppData folder
    media_player_path = os.path.join(
        os.getenv('LOCALAPPDATA'),
        'Microsoft',
        'WindowsApps',
        'Microsoft.ZuneMusic_8wekyb3d8bbwe',
        'MediaPlayer.exe'
    )
    # Open MediaPlayer.exe
    subprocess.Popen(media_player_path)
