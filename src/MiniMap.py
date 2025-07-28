import pyautogui
import pygetwindow as gw
from pywinauto import Desktop
import sys
import cv2
import numpy as np
import json
import logging
import os
from typing import Tuple
from PIL import ImageGrab
from utils.MinimapGrabber import ScreenCropper
from src.MiniMapConfigParser import MiniMapConfigParser
class MiniMap():
    MINIMAP_FILE_PATH = 'minimap_screenshot.png'
    MINIMAP_CONFIG_FILE_PATH = 'config\minimap_config.json'
    def __init__(self, application_name : str) -> None:
        self.application_name = application_name
        self._get_application_window_location()
        #self.setup_minimap_config()
        #self.find_minimap_candidates()
        
    def setup(self):
        screen_grabber = ScreenCropper()
        screen_grabber.run()
        self.minimap_coords = screen_grabber.get()
        self.screenshot_minimap()
        self._setup_maze_array((30,30))
    
    def _setup_maze_array(self, resize:Tuple = None):
        tolerance = 128
        img = cv2.imread(self.MINIMAP_FILE_PATH, cv2.IMREAD_GRAYSCALE)

        _, binary = cv2.threshold(img, tolerance, 255, cv2.THRESH_BINARY)

        maze_array = (binary // 255).astype(np.uint8)
        cv2.imwrite('bw-screenshot.png', binary)
        print(len(maze_array), len(maze_array[0]))
        if(resize):
            resized = cv2.resize(img, (resize[0], resize[1]), interpolation=cv2.INTER_AREA)
            for i in resized:
                for j in resize:
                    print(j)
        return maze_array
        
        
        
        
    def setup_minimap_config(self) -> None:
        
        
        try:
            with open(self.MINIMAP_CONFIG_FILE_PATH, "r") as f:
                config = json.load(f)
                self.config = MiniMapConfigParser(config)
                
        except FileNotFoundError:
            logging.error(f'File not found : Attempted file path {self.MINIMAP_CONFIG_FILE_PATH}')
            sys.exit(1)
        
    def screenshot_minimap(self):
        img = ImageGrab.grab(bbox=(self.minimap_coords['X'], 
                                   self.minimap_coords['Y'],
                                   self.minimap_coords['X'] + self.minimap_coords['WIDTH'], 
                                   self.minimap_coords['Y'] + self.minimap_coords['HEIGHT']))
        img.save(self.MINIMAP_FILE_PATH)
        
        pass
        
        
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
                            
    def _find_circle_minimap_canidate(self, screenshot_file_path: str):
        image = cv2.imread(screenshot_file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
        
        thresh = cv2.threshold(sharpen, 127, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        
        min_area = self.config.min_size
        max_area = self.config.max_size
        
        image_number = 0
        for c in cnts:
            area = cv2.contourArea(c)
            if area > min_area and area < max_area:
                x,y,w,h = cv2.boundingRect(c)
                print(x,y,w,h, w*h)
                cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
                image_number += 1
    
        cv2.imwrite('sharpen.png', sharpen)
        cv2.imwrite('close.png', close)
        cv2.imwrite('blur.png', blur)
        
        cv2.imwrite('thresh.png', thresh)
        cv2.imwrite("minimap_detected.png", image)
     
    def find_minimap_candidates(self):
            
        screenshot_file_path:str = 'Screenshot_TEMP.png'
        pyautogui.screenshot(region=(
            self.application_window.get('X'), 
            self.application_window.get('Y'), 
            self.application_window.get('Width'), 
            self.application_window.get('Height'))).save(screenshot_file_path)
        
        match self.config.shape:
            case 'square':
                self._find_square_minimap_canidate(screenshot_file_path=screenshot_file_path)
                
            case 'circle':
                self._find_circle_minimap_canidate(screenshot_file_path=screenshot_file_path)
        