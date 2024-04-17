
# from tkinter import *
# from PIL import Image, ImageTk

# class MyLabel(Label):
#     def __init__(self, master, filename):
#         im = Image.open(filename)
#         seq =  []
#         try:
#             while 1:
#                 seq.append(im.copy())
#                 im.seek(len(seq)) # skip to next frame
#         except EOFError:
#             pass # we're done

#         try:
#             self.delay = im.info['duration']
#         except KeyError:
#             self.delay = 100

#         first = seq[0].convert('RGBA')
#         self.frames = [ImageTk.PhotoImage(first)]

#         Label.__init__(self, master, image=self.frames[0])

#         temp = seq[0]
#         for image in seq[1:]:
#             temp.paste(image)
#             frame = temp.convert('RGBA')
#             self.frames.append(ImageTk.PhotoImage(frame))

#         self.idx = 0

#         self.cancel = self.after(self.delay, self.play)

#     def play(self):
#         self.config(image=self.frames[self.idx])
#         self.idx += 1
#         if self.idx == len(self.frames):
#             self.idx = 0
#         self.cancel = self.after(self.delay, self.play)

# class Main():
#     def __init__(self):
#         root = Tk()
#         self.anim = MyLabel(root, 'gifs\dog1.gif')
#         self.anim.pack()
#         Button(root, text='stop', command=self.stop_it).pack()
#         root.mainloop()

#     def stop_it(self):
#         self.anim.after_cancel(self.anim.cancel)


# main = Main()


import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageSequence

gif_filename = 'gifs\dog1.gif'

layout = [[sg.Image(key='-IMAGE-')]]

window = sg.Window('Window Title', layout, element_justification='c', margins=(0,0), element_padding=(0,0), finalize=True)

interframe_duration = Image.open(gif_filename).info['duration']

while True:
    for frame in ImageSequence.Iterator(Image.open(gif_filename)):
        event, values = window.read(timeout=interframe_duration)
        if event == sg.WIN_CLOSED:
            exit(0)
        window['-IMAGE-'].update(data=ImageTk.PhotoImage(frame) )