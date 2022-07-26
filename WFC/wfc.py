import random
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import os


def OpenImg(name: str, rotation_index: int) -> PhotoImage:
    global img, straight, cross, ninety, blank, three
    imgdir = os.getcwd() + "\\Assets\\" + name + ".png"
    img = Image.open(imgdir).resize((64,64), Image.ANTIALIAS)
    img = img.rotate((rotation_index - 1)*90)
    img = ImageTk.PhotoImage(img)
    if name == 'straight':
        straight['mesh'] = img
    elif name == 'cross':
        cross['mesh'] = img
    elif name == 'ninety':
        ninety['mesh'] = img
    elif name == 'blank':
        blank['mesh'] = img
    elif name == 'three':
        three['mesh'] = img

def UpdateGrid() -> None:
    no_rows = 2
    no_cols = 2
    labels = [None] * no_cols * no_rows

    global straight, cross, ninety, blank, three
    names = [blank, cross, ninety, straight, three]
    for i in range(no_cols * no_rows):
        r, c = divmod(i, no_cols)
        image = random.choice(names)['mesh']
        labels[i] = tkinter.Label(master=frame, image=image,  width=64, height=64, borderwidth=0)
        labels[i].grid(row=r, column=c)

# ---main---
img = 0
root = Tk()

straight = {}
cross = {}
ninety = {}
three = {}
blank = {}
OpenImg(name='straight', rotation_index=2)
OpenImg(name='cross', rotation_index=1)
OpenImg(name='ninety', rotation_index=1)
OpenImg(name='three', rotation_index=1)
OpenImg(name='blank', rotation_index=1)

root.geometry('700x700')

frame = tkinter.Frame(master=root)
frame.pack(expand=True)
UpdateGrid()
root.mainloop()