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
from sklearn.cluster import KMeans
import cv2
import numpy as np
from sklearn.cluster import KMeans
from src.Constants import MINIMAP_FILE_PATH, MINIMAP_CONFIG_FILE_PATH
import time
class MiniMap():

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
        self.config.overide_data(self.minimap_coords)
        

    def group_confident_colors(self, output_path='postprocess.png', num_colors=5, confidence_threshold=40):
        """
        Groups colors in an image and keeps only high-confidence pixels (close to cluster center).

        Args:
            input_path (str): Path to input image.
            output_path (str, optional): Path to save output.
            num_colors (int): Number of color clusters.
            confidence_threshold (int): Max Euclidean distance from cluster center to keep a pixel.

        Returns:
            np.ndarray: Image with confident color regions drawn.
        """
        start = time.time()
        img = cv2.imread(MINIMAP_FILE_PATH)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {MINIMAP_FILE_PATH}")

        h, w = img.shape[:2]
        data = img.reshape((-1, 3))

        # Fit KMeans
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init="auto")
        labels = kmeans.fit_predict(data)
        centers = kmeans.cluster_centers_
        clustered = labels.reshape((h, w))

        # Calculate distance of each pixel to its cluster center
        distances = np.linalg.norm(data - centers[labels], axis=1).reshape((h, w))

        output = np.zeros_like(img)

        for i in range(num_colors):
            mask = ((clustered == i) & (distances < confidence_threshold)).astype("uint8") * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            color = tuple(map(int, centers[i]))  # Use actual cluster color
            for cnt in contours:
                if cv2.contourArea(cnt) > 100:
                    cv2.drawContours(output, [cnt], -1, color, -1)
        
        if output_path:
            cv2.imwrite(output_path, output)
        
        print(time.time() - start , ' time elapsed')
        return output
    
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
        #self.group_confident_colors(num_colors=8, confidence_threshold=30)
        bgr_img = cv2.imread(MINIMAP_FILE_PATH)
        if bgr_img is None:
            raise FileNotFoundError(f"Image not found or unreadable: {MINIMAP_FILE_PATH}")

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
            with open(MINIMAP_CONFIG_FILE_PATH, "r") as f:
                config = json.load(f)
                self.config = MiniMapConfigParser(config)
                self.HAS_VALID_CONFIG = True
                
        except FileNotFoundError:
            logging.error(f'File not found : Attempted file path {MINIMAP_CONFIG_FILE_PATH}')
            sys.exit(1)
        
    def screenshot_minimap(self, resize: float = None):
        if(not self.HAS_VALID_CONFIG):
            logging.error('Config is not initialized properly')
            sys.exit(1)
            
        img = ImageGrab.grab(bbox=(self.config.X,
                                   self.config.Y,
                                   self.config.X + self.config.WIDTH,
                                   self.config.Y + self.config.HEIGHT))
        
        if(not resize):
            img.save(MINIMAP_FILE_PATH)
        else:
            resized_height = self.config.HEIGHT * resize
            resized_width = self.config.WIDTH * resize
            screenshot_np = np.array(img)  
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            resized = cv2.resize(screenshot_bgr, (int(resized_height), int(resized_width)), interpolation=cv2.INTER_AREA)
            cv2.imwrite(MINIMAP_FILE_PATH, resized)
            
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
                            