"this code is simply calculator"
from tkinter.ttk import Style

"first project of mine"
"    Creator: Snir Oded"


from tkinter import *
import tkinter as tk

def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))
def button_add_function():
    first_number = e.get()
    global f_num
    global math
    math = "addition"
    f_num = int(first_number)
    e.delete(0, END)
def button_substract_function():
    first_number = e.get()
    global f_num
    global math
    math = "subtraction"
    f_num = int(first_number)
    e.delete(0, END)
def button_multiply_function():
    first_number = e.get()
    global f_num
    global math
    math = "multiplication"
    f_num = int(first_number)
    e.delete(0, END)
def button_divide_function():
    first_number = e.get()
    global f_num
    global math
    math = "division"
    f_num = int(first_number)
    e.delete(0, END)

def button_equals():
    second_number = e.get()
    e.delete(0, END)
    if math == "addition":
         e.insert(0, f_num + int(second_number))
    if math == "subtraction":
         e.insert(0, f_num - int(second_number))
    if math == "multiplication":
         e.insert(0, f_num * int(second_number))
    if math == "division":
         e.insert(0, f_num / int(second_number))
def button_clear1():
    e.delete(0, END)

def tkinter_trying():
    root.title("Tkinter APP")
    # define buttons 0-9
    button_1 = Button(root, text="1", state=NORMAL, command=lambda: button_click(1), padx=10, pady=10)
    button_2 = Button(root, text="2", state=NORMAL, command=lambda: button_click(2), padx=10, pady=10)
    button_3 = Button(root, text="3", state=NORMAL, command=lambda: button_click(3), padx=10, pady=10)
    button_4 = Button(root, text="4", state=NORMAL, command=lambda: button_click(4), padx=10, pady=10)
    button_5 = Button(root, text="5", state=NORMAL, command=lambda: button_click(5), padx=10, pady=10)
    button_6 = Button(root, text="6", state=NORMAL, command=lambda: button_click(6), padx=10, pady=10)
    button_7 = Button(root, text="7", state=NORMAL, command=lambda: button_click(7), padx=10, pady=10)
    button_8 = Button(root, text="8", state=NORMAL, command=lambda: button_click(8), padx=10, pady=10)
    button_9 = Button(root, text="9", state=NORMAL, command=lambda: button_click(9), padx=10, pady=10)
    button_0 = Button(root, text="0", state=NORMAL, command=lambda: button_click(0), padx=10, pady=10)

    # define buttons +,-,*,/
    button_add = Button(root, text="+", state=NORMAL, command=button_add_function, padx=10, pady=10, fg="black", bg="#ffffff")
    button_substract = Button(root, text="-", state=NORMAL, command=button_substract_function, padx=10, pady=10, fg="black", bg="#ffffff")
    button_multiply = Button(root, text="*", state=NORMAL, command=button_multiply_function, padx=10, pady=10, fg="black", bg="#ffffff")
    button_divide = Button(root, text="/", state=NORMAL, command=button_divide_function, padx=10, pady=10, fg="black", bg="#ffffff")

    # define buttons =,C
    button_equal = Button(root, text="=", state=NORMAL, command=button_equals, padx=10, pady=10, fg="black", bg="#ffffff")
    button_clear = Button(root, text="C", state=NORMAL, command=button_clear1, padx=10, pady=10, fg="black", bg="#ffffff", style='btn_style')

    #Order Buttons

    button_1.grid(row=3, column=1)
    button_2.grid(row=3, column=2)
    button_3.grid(row=3, column=3)

    button_4.grid(row=2, column=1)
    button_5.grid(row=2, column=2)
    button_6.grid(row=2, column=3)

    button_7.grid(row=1, column=1)
    button_8.grid(row=1, column=2)
    button_9.grid(row=1, column=3)

    button_0.grid(row=4, column=2)
    button_clear.grid(row=0, column=0)
    button_add.grid(row=2, column=0)
    button_equal.grid(row=4, column=3)
    button_substract.grid(row=3, column=0)
    button_multiply.grid(row=4, column=0)
    button_divide.grid(row=5, column=0)
    root.mainloop()


# calling methods
root = Tk()
e = Entry(root, width=40, borderwidth=3)
# to add attribute - cursor font selectborderwidth
e.grid(row=0, column=1, columnspan=3, padx=20, pady=30)
# print(memory_game())
style = Style()


# This will be adding style, and
# naming that style variable as
# W.Tbutton (TButton is used for ttk.Button).
style.configure('btn_style', font=('calibri', 10, 'bold', 'underline'), foreground='red')

tkinter_trying()
