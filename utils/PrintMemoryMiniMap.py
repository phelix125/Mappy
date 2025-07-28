import numpy as np
import cv2
from typing import List

def array_to_image(array: List[List[int]], output_path: str = "INTERNAL_MINIMAP.png") -> None:
    """
    Converts a 2D integer array into an image with specified color mapping and saves it.

    Color Mapping:
        0 -> White
        1 -> Black
        2 -> Blue

    Args:
        array (List[List[int]]): 2D list of integers (0, 1, 2).
        output_path (str): File path where the image will be saved.
    """
  
    color_map = {
        0: (255, 255, 255),  # White
        1: (0, 0, 0),        # Black
        2: (255, 0, 0),      # Blue (OpenCV uses BGR)
    }

    height = len(array)
    width = len(array[0]) if height > 0 else 0

    
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for r in range(height):
        for c in range(width):
            color = color_map.get(array[r][c], (128, 128, 128))  #
            img[r, c] = color

    
    cv2.imwrite(output_path, img)
    