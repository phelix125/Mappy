import tkinter as tk
from PIL import ImageGrab
import pyautogui
import json
class ScreenCropper:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def on_mouse_down(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_mouse_drag(self, event):
        curr_x = self.canvas.canvasx(event.x)
        curr_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, curr_x, curr_y)

    def on_mouse_up(self, event):
        self.coordinates = {}
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        width = x2 - x1
        height = y2 - y1

        self.coordinates['X'] = (int(x1))
        self.coordinates['Y'] = (int(y1))
        self.coordinates['WIDTH'] = int(width)
        self.coordinates['HEIGHT'] = int(height)
        print(f' X: {x1} Y: {y1} WIDTH: {width} HEIGHT: {height}')


        self.root.destroy()

    def run(self):
        self.root.mainloop()
        
    def get(self):
        return self.coordinates

if __name__ == "__main__":
    cropper = ScreenCropper()
    cropper.run()