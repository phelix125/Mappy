import pyautogui
import pygetwindow as gw
from pywinauto import Desktop
import sys
import cv2
import numpy as np
from MiniMap import MiniMap
class Mappy():
    def __init__(self, application_name: str, shape: str):
        self.minimap = MiniMap(application_name = application_name, shape=shape)
        pass
    
    


    
    def locate_map(self):
        pass