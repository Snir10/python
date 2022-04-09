from tkinter import *

ws = Tk()
ws.title('PythonGuides')
ws.geometry('150x150')
ws.config(bg='#F2B90F')

def display_selected(choice):
    choice = variable.get()
    print(choice)

countries = ['Bahamas','Canada', 'Cuba','United States']

# setting variable for Integers
variable = StringVar()
variable.set(countries[3])

# creating widget
dropdown = OptionMenu(ws, variable, *countries, command=display_selected)

# positioning widget
dropdown.pack(expand=True)

# infinite loop 
ws.mainloop()
