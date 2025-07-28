import tkinter as tk
from PIL import Image, ImageGrab, ImageTk, ImageDraw
import pyautogui

ZOOM_SCALE = 12
MAG_SIZE = 15  # should be odd so the center pixel is exact
PREVIEW_SIZE = 60  # size of the color preview square

class PixelPicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="white")

        self.canvas = tk.Canvas(self.root, width=MAG_SIZE*ZOOM_SCALE, height=MAG_SIZE*ZOOM_SCALE, highlightthickness=1, highlightbackground="black")
        self.canvas.grid(row=0, column=0, padx=5, pady=5)

        self.color_preview = tk.Canvas(self.root, width=PREVIEW_SIZE, height=PREVIEW_SIZE, highlightthickness=1, highlightbackground="black")
        self.color_preview.grid(row=0, column=1, padx=5, pady=5)

        self.rgb_label = tk.Label(self.root, text="RGB: (0, 0, 0)", font=("Arial", 12), bg="white")
        self.rgb_label.grid(row=1, column=0, columnspan=2, pady=(0,5))

        self.root.bind("<Button-1>", self.on_left_click)
        self.root.bind("<Button-3>", self.on_right_click)

        self.last_rgb = (0, 0, 0)
        self.is_running = True

        self.update_loop()

    def on_left_click(self, event):
        print(f"Left click detected! RGB: {self.last_rgb}")

    def on_right_click(self, event):
        print("Right click detected! Exiting.")
        self.is_running = False
        self.root.destroy()

    def update_loop(self):
        if not self.is_running:
            return

        x, y = pyautogui.position()

        left = x - MAG_SIZE//2
        top = y - MAG_SIZE//2
        right = left + MAG_SIZE
        bottom = top + MAG_SIZE
        screen = ImageGrab.grab(bbox=(left, top, right, bottom))

        zoomed = screen.resize((MAG_SIZE*ZOOM_SCALE, MAG_SIZE*ZOOM_SCALE), Image.NEAREST)

        draw = ImageDraw.Draw(zoomed)
        center = (MAG_SIZE*ZOOM_SCALE)//2
        draw.line((center, 0, center, MAG_SIZE*ZOOM_SCALE), fill="red")
        draw.line((0, center, MAG_SIZE*ZOOM_SCALE, center), fill="red")

        tk_img = ImageTk.PhotoImage(zoomed)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=tk_img)
        self.canvas.image = tk_img

        center_pixel = screen.getpixel((MAG_SIZE//2, MAG_SIZE//2))
        self.last_rgb = center_pixel
        self.rgb_label.config(text=f"RGB: {center_pixel}")

        hex_color = '#%02x%02x%02x' % center_pixel
        self.color_preview.delete("all")
        self.color_preview.create_rectangle(0, 0, PREVIEW_SIZE, PREVIEW_SIZE, fill=hex_color, outline='black')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        win_x = x + 20
        win_y = y + 20
        if win_x + MAG_SIZE*ZOOM_SCALE + PREVIEW_SIZE + 20 > screen_width:
            win_x = x - (MAG_SIZE*ZOOM_SCALE + PREVIEW_SIZE + 30)
        if win_y + MAG_SIZE*ZOOM_SCALE + 50 > screen_height:
            win_y = y - (MAG_SIZE*ZOOM_SCALE + 70)
        self.root.geometry(f"+{win_x}+{win_y}")

        self.root.after(30, self.update_loop)


if __name__ == "__main__":
    picker = PixelPicker()
    picker.root.mainloop()
