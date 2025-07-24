import pyautogui
import pygetwindow as gw
from pywinauto import Desktop
import sys
import cv2
import numpy as np
import json
import logging
import os

class MiniMapConfigParser():
    SHAPE = 'shape'
    QUADRANT = 'quadrant'
    MIN_SIZE = 'min_size'
    MAX_SIZE = 'min_size'
    def __init__(self, data: dict):
        self.data = data
        pass
    
    def validate_config_values(self):
        CONFIG_KEYS = [self.SHAPE, self.QUADRANT, self.MIN_SIZE, self.MAX_SIZE]
        
        for index, (key,value) in enumerate(self.data.items()):
            match key:
                case self.SHAPE:
                    if(value.lower() not in ['circle', 'square']):
                        logging.error('')
                    
        
    
    def is_valid_integer_input(self, value:int | float, min: int | float, max: int | float):
        if(min < value and value < max):
            return True
        else:
            return False
            
class MiniMap():
    def __init__(self, application_name : str) -> None:
        self.application_name = application_name
        self._get_application_window_location()
        self.setup_minimap_config()
        self.find_minimap_candidates()
        
    def setup_minimap_config(self) -> None:
        
        config_path:str = "config\minimap_config.json"
        
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                
        except FileNotFoundError:
            logging.error(f'File not found : Attempted file path {config_path}')
            sys.exit(1)
        

    def _get_application_window_location(self):
        windows = Desktop(backend="win32").windows()
        for win in windows:
            if self.application_name in win.window_text():
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
                   
    def _find_square_minimap_canidate(self, screenshot_file_path: str):
        img = cv2.imread(screenshot_file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        output_img = img.copy()

        edged = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4 and cv2.contourArea(cnt) > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = w / float(h)
                if 0.8 <= aspect_ratio <= 1.2:  # Likely square
                    print(f"[Square] Minimap candidate at ({x}, {y}) size ({w}, {h})")
                    cv2.rectangle(output_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imwrite("minimap_detected.png", output_img)
             
    def _find_circle_minimap_canidate(self, screenshot_file_path: str):
        img = cv2.imread(screenshot_file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        output_img = img.copy()

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=100,
            param1=80,
            param2=50,
            minRadius=50,
            maxRadius=150
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                x, y, r = i
                print(f"[Circle] Minimap candidate at ({x}, {y}) with radius {r}")
                cv2.rectangle(output_img, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)
        else:
            print("No circular minimap candidates found.")
            
        cv2.imwrite("minimap_detected.png", output_img)
        
    def find_minimap_candidates(self):
        
        if(self.config['shape'].lower() not in ['square', 'circle']):
            print('Invalid shape')
            sys.exit()
            
        screenshot_file_path:str = 'Screenshot_TEMP.png'
        pyautogui.screenshot(region=(
            self.application_window.get('X'), 
            self.application_window.get('Y'), 
            self.application_window.get('Width'), 
            self.application_window.get('Height'))).save(screenshot_file_path)
        
        match self.config['shape'].lower():
            case 'square':
                self._find_square_minimap_canidate(screenshot_file_path=screenshot_file_path)
                
            case 'circle':
                self._find_circle_minimap_canidate(screenshot_file_path=screenshot_file_path)
        