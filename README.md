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

| ![Website Thumbnail](/assets/thumbnail.PNG) | **VAHCINET Functional Buttons:** |
|------------------------------------------------|------------------------------------|
| **Search Button:** Imitates the Windows Search button. |
| **Upload Button:** Opens the Default Browser and will navigate to Google Drive. |
| **LMS Button:** Opens up the CDM LMS Blackboard using Default Browser. |
| **Files Button:** Opens the File Manager and automatically clicks the search panel. |
| **Browser Button:** Opens the Default Browser and will navigate to Google. |
| **Eye-tracker Button:** This button activates the Eye tracker, which allows manual control of the mouse cursor using the user's eye and head movements. |
| **Voice Command Button:** Activates the HCI system that allows computer navigation using voice inputs. |
| **Command List:** Opens a pop-up containing the available voice commands the application can perform. |
| **Microsoft Tools:** This button opens a pop-up menu for common tools for students. |
| **Music Button:** Opens the default media player of the computer. |


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


