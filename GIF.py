import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

class GIF(tk.Label):
    def __init__(self, master, filename, width=None, height=None, *args, **kwargs):
        im = Image.open(filename)
        self.frames = []

        # Resizing images if width and height are provided
        if width and height:
            im = im.resize((width, height), Image.LANCZOS)

        try:
            for i in count(1):
                # Ensure all frames are resized if needed
                frame = im.copy()
                if width and height:
                    frame = frame.resize((width, height), Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame))
                im.seek(i)
        except EOFError:
            pass

        super().__init__(master, image=self.frames[0], *args, **kwargs)

        self.current_frame = 0
        self.ani_delay = im.info['duration']  # Retrieves delay in milliseconds
        self.update_animation()

    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.configure(image=self.frames[self.current_frame])
        self.after(self.ani_delay, self.update_animation)
