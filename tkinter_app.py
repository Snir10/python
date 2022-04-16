"this code is simply calculator"
"first project of mine"
"    Creator: Snir Oded"
import time
from tkinter import *

def search_func():
    e.delete(0, END)
    e.insert(0, 'clicked!')
    time.sleep(1)
    e.delete(0, END)
    selection = "option: " + str(optionVar.get()+' | '+v.get()+' | '+str(scal.get())+' | '+str(spinboxVar.get()))
    e.insert(0, selection)
    print("searched")

def option_menu_func(optionVar):
    print('option manu')

def setting_func():
    print('settings clicked')
    window = Toplevel()
    window.geometry('250x250')
    window.resizable(0, 0)
    newlabel = Label(window, text="Settings Window\n TODO more actions")
    newlabel.pack()

def sel():
    print("radio choosed")

def scal_func(scal_val):
    print('scal_val')

def spinbox_func(var):
    print(str(var))

def tkinter_trying():
    root.title("Tkinter APP")
    root.geometry("600x400")
    root.resizable(0, 0)


    headline = Label(root, height=2, width=10, font='Helvetica 28 bold', text='Snirs APP', bg='#DDDDDD', fg='#343434')

    radiobutton2 = Radiobutton(root, height=1, padx=2, pady=2, text='NO', bg='#111111',fg='#AAAAAA', state=NORMAL, command=sel, variable=v, value="NO")
    radiobutton1 = Radiobutton(root, height=1, padx=2, pady=2, text='YES', bg='#BBBBBB', state=ACTIVE, command=sel, variable=v, value="YES")
    
    dropdown = OptionMenu(root, optionVar, *countries, command=option_menu_func(optionVar))

    spinbox = Spinbox(root, from_=0, to=10, textvariable=spinboxVar)

    scroller = Scale(root, width=15, orient=HORIZONTAL, variable=scal, command=scal_func(scal))

    button_search = Button(root, text="Search", state=NORMAL, command=search_func, padx=10, pady=10, fg="black", bg="#ffffff")
    button_settings = Button(root, text="settings", state=NORMAL, command=setting_func, padx=10, pady=10, fg="black", bg="#ffffff")

    #Order Buttons
    headline.grid(row=0, column=0)
    dropdown.grid(row=1, column=0)
    e.grid(row=1, column=1, columnspan=3, padx=20, pady=30)

    scroller.grid(row=5, column=1, rowspan=2)

    radiobutton1.grid(row=5, column=0)
    radiobutton2.grid(row=6, column=0)

    button_search.grid(row=7, column=0)
    button_settings.grid(row=7, column=1)

    spinbox.grid(row=4, column=0)



    root.mainloop()


# calling methods
root = Tk()
e = Entry(root, width=25, borderwidth=3)


countries = ['All', 'Bahamas', 'Canada', 'Cuba', 'United States', 'Mexico', 'Japan', 'China']


# setting variable for Integers
optionVar = StringVar()
optionVar.set(countries[0])
v = StringVar()
scal = IntVar()
spinboxVar = IntVar()

#running main software
tkinter_trying()

