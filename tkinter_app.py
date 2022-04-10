"this code is simply calculator"
import time
from tkinter import ttk

"first project of mine"
"    Creator: Snir Oded"


from tkinter import *
def button_search():
    e.delete(0, END)
    e.insert(0, 'clicked!')
    time.sleep(1)
    e.delete(0, END)
    selection = "option: " + str(variable.get()+'\t'+v.get()+'\t'+str(scal.get()))
    e.insert(0, selection)
    print("searched")

def setting_func():
    window = Toplevel()
    window.geometry('250x250')
    newlabel = Label(window, text="Settings Window\n TODO more actions")
    newlabel.pack()


def sel():
    # e.delete(0, END)
    # selection = "option: " + str(variable.get())
    # e.insert(0, selection)
    print("radio choosed")

def scal_func(scal_val):
    print(scal_val)

def tkinter_trying():
    root.title("Tkinter APP")
    root.geometry("600x600")


    headline = Label(root, height=2, width=10, font='Helvetica 40 bold', text='Snirs APP')

    radiobutton2 = Radiobutton(root, height=1, padx=2, pady=2, text='NO', bg='#77BBBB', state=NORMAL, command=sel, variable=v, value="NO")
    radiobutton1 = Radiobutton(root, height=1, padx=2, pady=2, text='YES', bg='#77BBBB', state=ACTIVE, command=sel, variable=v, value="YES")
    
    dropdown = OptionMenu(root, variable, *countries)

    scroller = Scale(root, width=15, orient=HORIZONTAL, variable=scal, command=scal_func(scal))

    button_clear = Button(root, text="Search", state=NORMAL, command=button_search, padx=10, pady=10, fg="black", bg="#ffffff")
    button_settings = Button(root, text="settings", state=NORMAL, command=setting_func, padx=10, pady=10, fg="black", bg="#ffffff")

    #Order Buttons
    headline.grid(row=0, column=0, columnspan=4)
    dropdown.grid(row=2, column=0)
    button_clear.grid(row=8, column=0)
    scroller.grid(row=7, column=0)

    radiobutton1.grid(row=5, column=0)
    radiobutton2.grid(row=6, column=0)
    button_settings.grid(row=6, column=1)


    e.grid(row=2, column=1, columnspan=2, padx=20, pady=30)

    root.mainloop()


# calling methods
root = Tk()
e = Entry(root, width=40, borderwidth=3)


countries = ['All', 'Bahamas', 'Canada', 'Cuba', 'United States', 'Mexico', 'Japan', 'China']


# setting variable for Integers
variable = StringVar()
variable.set(countries[0])
v = StringVar()
scal = IntVar()
tkinter_trying()
