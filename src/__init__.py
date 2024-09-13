from .Search import open_Search
from .Upload import open_Upload
from .LMS import open_LMS
from .Files import open_Files
from .Browser import open_Browser
# from .EyeTracker import eyeTrackerFunction
# from .VoiceCommand import voiceCommandFunction
from .CommandList import open_CommandList
from .Office import open_MsOfficePopup
from .Music import open_Music

function_map = {
    "open_Search": open_Search,
    "open_Upload": open_Upload,
    "open_LMS": open_LMS,
    "open_Files": open_Files,
    "open_Browser": open_Browser,
    # "eyeTrackerFunction": eyeTrackerFunction,
    # "voiceCommandFunction": voiceCommandFunction,
    "open_CommandList": open_CommandList,
    "open_MsOfficePopup": open_MsOfficePopup,
    "open_Music": open_Music
}
