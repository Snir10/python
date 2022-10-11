
from tkinter import *
from PIL import Image, ImageTk


root = Tk()

frame = LabelFrame(root, text="this is my frame", padx=50, pady=50)
frame.pack(padx=100, pady=100)

b = Button(frame, text="don't click here")
b2 = Button(frame, text="click here")
b.grid(row=0, column=0, columnspan=2)
b2.grid(row=1, column=0, columnspan=2)

root.mainloop()