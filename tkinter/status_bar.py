
from tkinter import *
from PIL import Image, ImageTk


def forward(image_number):
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number-1])
    button_forward = Button(root, text=">>", command=lambda: forward(image_number+1))
    button_back = Button(root, text="<<", command=lambda: back(image_number-1))

    if image_number == 5:
        button_forward = Button(root, text=">>", state=DISABLED)

    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)

    status = Label(root, text="Images "+str(image_number)+" of " + str(len(image_list)), relief=SUNKEN, anchor=E)
    status.grid(row=5, column=0, columnspan=3, sticky=W+E)


def back(image_number):
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number-1])
    button_forward = Button(root, text=">>", command=lambda: forward(image_number+1))
    button_back = Button(root, text="<<", command=lambda: back(image_number-1))

    if image_number == 1:
        button_back = Button(root, text="<<", state=DISABLED)

    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)

    status = Label(root, text="Images "+str(image_number)+" of " + str(len(image_list)), relief=SUNKEN, anchor=E)
    status.grid(row=5, column=0, columnspan=3, sticky=W+E)

root = Tk()

my_img1 = ImageTk.PhotoImage(Image.open("C:/pics/Car1.jpg"))
my_img2 = ImageTk.PhotoImage(Image.open("C:/pics/Car2.jpg"))
my_img3 = ImageTk.PhotoImage(Image.open("C:/pics/Car3.jpg"))
my_img4 = ImageTk.PhotoImage(Image.open("C:/pics/Car4.jpg"))
my_img5 = ImageTk.PhotoImage(Image.open("C:/pics/Car5.jpg"))

image_list = [my_img1, my_img2, my_img3, my_img4, my_img5]

status = Label(root, text="Images 1 of " + str(len(image_list)), relief=SUNKEN, anchor=E)

my_label = Label(image=my_img1)
my_label.grid(row=0, column=0, columnspan=3)



button_exit = Button(root, text="Exit Program", command=root.quit)
button_back = Button(root, text="<<", command=back, state=DISABLED)


button_forward = Button(root, text=">>", command=lambda: forward(2))

button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_forward.grid(row=1, column=2)
status.grid(row=5, column=0, columnspan=3, sticky=W+E)


root.mainloop()