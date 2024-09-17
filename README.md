# VAHCINET: Voice Activated Human Computer Interaction using Convolutional Neural Networks Algorithm
**Authors:** Escobar, R. C., Razo, I. W., Tabusao, F. I

**Overview:** A Human-Computer Interaction system utilizing custom datasets trained in EdgeImpulse, classifying 34 HCI-based voice commands to perform computer navigations with a Convolutional Neural Network (CNN) algorithm.

## Running the VAHCINET Application

To run the VAHCINET, follow these steps:

**Open the Application:**
   - Open any IDE and run `main.py`.

   **Or use the following command:**

   ```bash
   pip install -r requirements.txt

   pyinstaller --name VAHCINET --onefile -w --icon=favicon.ico \
   --add-binary ".venv/Lib/site-packages/cv2/opencv_videoio_ffmpeg4100_64.dll;cv2" \
   --add-data ".venv/Lib/site-packages/mediapipe;mediapipe" \
   main.py
   ```

**This will create the .exe file of our application, located at dist folder.**
**Then, transfer the folders: assets, config, data, model, src to dist (Will replace this with an MSI installer)**

## VAHCINET Functional Buttons:

<table>
  <tr>
    <td rowspan="10" style="vertical-align: middle; text-align: center;"><img src="/assets/thumbnail.PNG" alt="Website Thumbnail" style="width:150px;"></td>
    <td><strong>Search Button:</strong> Imitates the Windows Search button.</td>
  </tr>
  <tr>
    <td><strong>Upload Button:</strong> Opens the Default Browser and will navigate to Google Drive.</td>
  </tr>
  <tr>
    <td><strong>LMS Button:</strong> Opens up the CDM LMS Blackboard using Default Browser.</td>
  </tr>
  <tr>
    <td><strong>Files Button:</strong> Opens the File Manager and automatically clicks the search panel.</td>
  </tr>
  <tr>
    <td><strong>Browser Button:</strong> Opens the Default Browser and will navigate to Google.</td>
  </tr>
  <tr>
    <td><strong>Eye-tracker Button:</strong> This button activates the Eye tracker, which allows manual control of the mouse cursor using the user's eye and head movements.</td>
  </tr>
  <tr>
    <td><strong>Voice Command Button:</strong> Activates the HCI system that allows computer navigation using voice inputs.</td>
  </tr>
  <tr>
    <td><strong>Command List:</strong> Opens a pop-up containing the available voice commands the application can perform.</td>
  </tr>
  <tr>
    <td><strong>Microsoft Tools:</strong> This button opens a pop-up menu for common tools for students.</td>
  </tr>
  <tr>
    <td><strong>Music Button:</strong> Opens the default media player of the computer.</td>
  </tr>
</table>




# VAHCINET List of Voice Commands:
VAHCINET will wait for 5 seconds to capture input voices and automatically navigates the computer based on the voice command.
 - Open Microsoft Word
 - Exit Microsoft Word
 - Open Microsoft Excel
 - Exit Microsoft Excel
 - Open Powerpoint
 - Exit Powerpoint
 - Open Zoom App
 - Exit Zoom App
 - Open Google
 - Exit Google
 - Open Calculator
 - Exit Calculator
 - Open Calendar
 - Exit Calendar
 - Open File Manager
 - Exit File Manager
 - Open Sticky Notes
 - Exit Sticky Notes
 - Open Notepad
 - Exit Notepad
 - Open Camera
 - Exit Camera
 - Open Paint
 - Exit Paint
 - Open Voice Recorder
 - Exit Voice Recorder
 - Open Google and Search <User Define> (i.e. Cats)
 - Open Youtube and Search <User Define> (i.e. Cats)
 - Open Browser and Search <User Define> (i.e. Cats)
 - Save File
 - Open Folder Downloads
 - Open File Documents
 - Print 
 - Shutdown Computer


