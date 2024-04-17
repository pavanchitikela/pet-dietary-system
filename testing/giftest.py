import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import time

class GIF(tk.Label):
    def __init__(self, master, filename, *args, **kwargs):
        im = Image.open(filename)
        self.frames = []
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
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

def main():
    root = tk.Tk()
    lbl = GIF(root, 'gifs\dog1.gif')
    lbl.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
