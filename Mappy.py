import pygetwindow as gw
from pywinauto import Desktop
import sys
class Mappy():
    def __init__(self, application_name: str):
        self.application_window = None
        self.get_application_window_location(application_name)
        pass
    
    def get_application_window_location(self, application_name: str):
        windows = Desktop(backend="win32").windows()
        for win in windows:
            if application_name in win.window_text():
                window = win.rectangle()
                self.application_window = {
                    'X':window.left,
                    'Y':window.top,
                    'Width': window.width(),
                    'Height': window.height()
                }
                break
        else:
            print("Window not found.")
            sys.exit()
        

    
 