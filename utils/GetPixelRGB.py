import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import tkinter as tk

def get_pixel_rgb_on_click():
    """
    Opens a fullscreen transparent overlay that lets the user click anywhere on the screen
    and retrieves the RGB value of the clicked pixel.

    Returns:
        tuple: (x, y, (R, G, B)) coordinates and RGB color of the clicked pixel.
    """
    clicked_position = {}

    def on_click(event):
        # Save mouse position
        clicked_position['x'] = event.x_root
        clicked_position['y'] = event.y_root
        root.destroy()

    # Create a transparent fullscreen window
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.01)  # Fully transparent to clicks
    root.configure(bg='black')
    root.bind("<Button-1>", on_click)

    print("Click anywhere on the screen to get the pixel RGB value...")
    root.mainloop()

    # Grab the pixel color from screen at clicked coordinates
    x, y = clicked_position['x'], clicked_position['y']
    screen = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    rgb = screen.getpixel((0, 0))

    print(f"Clicked at ({x}, {y}) — RGB: {rgb}")
    return x, y, rgb

get_pixel_rgb_on_click()