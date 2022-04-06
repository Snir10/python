from tkinter import *
import sqlite3

root = Tk()
root.title('Snir\'s SQL APP')
#root.iconbitmap('c:/X/X')
root.geometry("400x600")

#Databases
conn = sqlite3.connect('address_book.db')
#conn = sqlite3.connect('address_book1.db')

# Create cursor instanse
c = conn.cursor()


# when needs to crate a table

# c.execute("""CREATE TABLE addresses (
#     first_name text,
#     last_name text,
#     address text,
#     city text,
#     state text,
#     zipcode text)
#
#
#
#
#
# """)


def query():
    #create a DB or connect to one.
    conn = sqlite3.connect('address_book.db')

    # Create cursor instanse
    c = conn.cursor()

    #Query the database
    c.execute("SELECT oid, * FROM addresses")
    records = c.fetchall()
    print(records)
    print_records = ''

    for record in records:
        print_records += str(record[0]) +" "+str(record[1])+" "+str(record[2])+" "+str(record[3])+" "+str(record[4])+"\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=13, column=0, columnspan=2)

    # Commit Changes
    conn.commit()
    # close Changes
    conn.close()

def delete():
    #create a DB or connect to one.
    conn = sqlite3.connect('address_book.db')

    # Create cursor instanse
    c = conn.cursor()

    c.execute("DELETE from addresses WHERE oid = " + str(delete_box.get()))

    #erase field
    delete_box.delete(0, END)

    #Commit Changes
    conn.commit()
    #close Changes
    conn.close()

def submit():
    #create a DB or connect to one.
    conn = sqlite3.connect('address_book.db')

    # Create cursor instanse
    c = conn.cursor()

    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
      {
       'f_name': f_name.get(),
       'l_name': l_name.get(),
       'address': address.get(),
       'city': city.get(),
       'state': state.get(),
       'zipcode': zipcode.get()
        })

    # Commit Changes
    conn.commit()
    # close Changes
    conn.close()

    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)
#Create edit function to update our records
def edit():
    global editor
    editor = Tk()
    editor.title('Snir\'s SQL APP - EDITOR')
    # root.iconbitmap('c:/X/X')
    editor.geometry("400x200")

    # Databases
    conn = sqlite3.connect('address_book.db')

    # Create cursor instanse
    c = conn.cursor()

    record_id = delete_box.get()

    #Query the database
    c.execute("SELECT * FROM addresses WHERE oid = "+ record_id)

    records = c.fetchall()


    #Create Global Variables For Text Box Names
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor

    f_name_editor = Entry(editor, width=30)
    #f_name_editor.grid(row=0, column=1, padx=20)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1)
    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1)

    # Create TextBox labels
    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row=0, column=0)
    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row=1, column=0)
    address_label = Label(editor, text="Address")
    address_label.grid(row=2, column=0)
    city_label = Label(editor, text="City")
    city_label.grid(row=3, column=0)
    state_label = Label(editor, text="State")
    state_label.grid(row=4, column=0)
    zipcode_label = Label(editor, text="ZipCode")
    zipcode_label.grid(row=5, column=0)
    #Loop thru results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    # Ceate a Edit button
    edit_btn = Button(editor, text="save Record", command=update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

def update():

    # Databases
    conn = sqlite3.connect('address_book.db')
    # Create cursor instanse
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE addresses SET 
    first_name = :first,
    last_name = :last,
    address = :address,
    city = :city,
    state = :state,
    zipcode = :zipcode
    
    WHERE oid = :oid""",
    {
    'first': f_name_editor.get(),
    'last': l_name_editor.get(),
    'address': address_editor.get(),
    'city': city_editor.get(),
    'state': state_editor.get(),
    'zipcode': zipcode_editor.get(),
    'oid': record_id


    })
    
    


    #Commit Changes
    conn.commit()
    #Close Connection
    conn.close()
    #Destroy Editor Window
    editor.destroy()


f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)
address = Entry(root, width=30)
address.grid(row=2, column=1)
city = Entry(root, width=30)
city.grid(row=3, column=1)
state = Entry(root, width=30)
state.grid(row=4, column=1)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1)

# edit_box = Entry(root, width=30)
# edit_box.grid(row=11, column=1)

#Create TextBox labels
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0)
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)
address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)
city_label = Label(root, text="City")
city_label.grid(row=3, column=0)
state_label = Label(root, text="State")
state_label.grid(row=4, column=0)
zipcode_label = Label(root, text="ZipCode")
zipcode_label.grid(row=5, column=0)

delete_label = Label(root, text="Select ID")
delete_label.grid(row=9, column=0)

# edit_label = Label(root, text="Edit ID")
# edit_label.grid(row=11, column=0)

#Create Submit Button.
submit_btn = Button(root, text="Add Record To DB", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create a Query Button.
query_btn = Button(root, text="Show records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)


#Ceate a Delete button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

#Ceate a Edit button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

#close Changes
conn.close()


root.mainloop()