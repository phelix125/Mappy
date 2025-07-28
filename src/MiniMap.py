import pygetwindow as gw
from pywinauto import Desktop
import sys
import cv2
import numpy as np
import json
import logging
from typing import Tuple, Dict
from PIL import ImageGrab
from utils.MinimapGrabber import ScreenCropper
from src.MiniMapConfigParser import MiniMapConfigParser

class MiniMap():
    MINIMAP_FILE_PATH = 'minimap_screenshot.png'
    MINIMAP_CONFIG_FILE_PATH = 'config\minimap_config.json'
    HAS_VALID_CONFIG = False
    
    def __init__(self, application_name : str) -> None:
        self.application_name = application_name
        self._get_application_window_location()
        self.setup_minimap_config()
        
    def setup(self):
        """
        This function must be called before using any function in this class.
        """
        screen_grabber = ScreenCropper()
        screen_grabber.run()
        self.minimap_coords = screen_grabber.get()
    
    
    def setup_internal_mini_map(
    self,
    rgb_to_label: Dict[Tuple[int, int, int], int],
    default_label: int = 0,
    tolerance: int = 10
) -> np.ndarray:
        """
        Set's up MiniMaps internal minimap, used for pathtracking. Itterates through the minimap
        and scans each RGB value and sets it to a diffierent value
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
            lower_bound = np.array([c - tolerance for c in target_rgb])
            upper_bound = np.array([c + tolerance for c in target_rgb])

            lower_bound = np.clip(lower_bound, 0, 255)
            upper_bound = np.clip(upper_bound, 0, 255)

            mask = np.all((rgb_img >= lower_bound) & (rgb_img <= upper_bound), axis=-1)

            label_array[mask] = label
  
        return label_array
        
    def setup_minimap_config(self) -> None:
        
        try:
            with open(self.MINIMAP_CONFIG_FILE_PATH, "r") as f:
                config = json.load(f)
                self.config = MiniMapConfigParser(config)
                self.HAS_VALID_CONFIG = True
                
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
                            