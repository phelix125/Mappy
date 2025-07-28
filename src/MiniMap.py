import pyautogui
import pygetwindow as gw
from pywinauto import Desktop
import sys
import cv2
import numpy as np
import json
import logging
import os
from typing import Tuple, Dict
from PIL import ImageGrab
from utils.MinimapGrabber import ScreenCropper
from src.MiniMapConfigParser import MiniMapConfigParser
from utils.PrintMemoryMiniMap import array_to_image
class MiniMap():
    MINIMAP_FILE_PATH = 'minimap_screenshot.png'
    MINIMAP_CONFIG_FILE_PATH = 'config\minimap_config.json'
    def __init__(self, application_name : str) -> None:
        self.application_name = application_name
        self._get_application_window_location()
        self.setup_minimap_config()
        
    def setup(self):
        screen_grabber = ScreenCropper()
        screen_grabber.run()
        self.minimap_coords = screen_grabber.get()
    
    def _setup_maze_array(self, resize:Tuple = None):
        self.screenshot_minimap()
        tolerance = 128
        img = cv2.imread(self.MINIMAP_FILE_PATH, cv2.IMREAD_GRAYSCALE)

        _, binary = cv2.threshold(img, tolerance, 255, cv2.THRESH_BINARY)

        maze_array = (binary // 255).astype(np.uint8)
        cv2.imwrite('bw-screenshot.png', binary)
        if(resize):
            resized = cv2.resize(img, (resize[0], resize[1]), interpolation=cv2.INTER_AREA)
            for i in resized:
                for j in resize:
                    pass
        return maze_array
    
    def convert_image_to_label_array(
    self,
    rgb_to_label: Dict[Tuple[int, int, int], int],
    default_label: int = 0,
    tolerance: int = 10
) -> np.ndarray:
        """
        Converts an image into a labeled array using RGB values, allowing for tolerance in color matching.

        Args:
            image_path (str): Path to the image file.
            rgb_to_label (Dict[Tuple[int, int, int], int]): Dictionary mapping RGB tuples to integer labels.
            default_label (int): Label for pixels that don't match any RGB value.
            tolerance (int): Tolerance for RGB matching (0–255). A pixel matches if each channel is within ±tolerance.

        Returns:
            np.ndarray: 2D array of labels.
        """

        bgr_img = cv2.imread(self.MINIMAP_FILE_PATH)
        if bgr_img is None:
            raise FileNotFoundError(f"Image not found or unreadable: {self.MINIMAP_FILE_PATH}")

        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        height, width, _ = rgb_img.shape
        label_array = np.full((height, width), default_label, dtype=np.int32)

        for target_rgb, label in rgb_to_label.items():
            # Compute boolean mask where the color is within the tolerance
            lower_bound = np.array([c - tolerance for c in target_rgb])
            upper_bound = np.array([c + tolerance for c in target_rgb])

            # Clip values to valid range [0, 255]
            lower_bound = np.clip(lower_bound, 0, 255)
            upper_bound = np.clip(upper_bound, 0, 255)

            # Generate mask for color within bounds
            mask = np.all((rgb_img >= lower_bound) & (rgb_img <= upper_bound), axis=-1)

            # Apply label
            label_array[mask] = label

        array_to_image(label_array)  
        return label_array
        
    def setup_minimap_config(self) -> None:
        
        try:
            with open(self.MINIMAP_CONFIG_FILE_PATH, "r") as f:
                config = json.load(f)
                self.config = MiniMapConfigParser(config)
                
        except FileNotFoundError:
            logging.error(f'File not found : Attempted file path {self.MINIMAP_CONFIG_FILE_PATH}')
            sys.exit(1)
        
    def screenshot_minimap(self):
        if(self.config is None):
            logging.error('Config is not initialized properly')
            sys.exit(1)
        img = ImageGrab.grab(bbox=(self.config.X,
                                   self.config.Y,
                                   self.config.X + self.config.WIDTH,
                                   self.config.Y + self.config.HEIGHT))
        img.save(self.MINIMAP_FILE_PATH)
        
        
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
                            