from tkinter import *
import sqlite3 
from tkinter import messagebox

from pkg_resources import ensure_directory
root= Tk()

root.title("Database")

conn= sqlite3.connect("address_book.db")
c=conn.cursor()

# c.execute(""" CREATE TABLE addresses(
#     first_name text,
#     last_name text,
#     address text,
#     city text,
#     state text,
#     zipcode integer
# )""")
# print("Table created successfully")

def submit():
    conn=sqlite3.connect("address_book.db")
    c=conn.cursor()

    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",{
        "f_name":f_name.get(),
        "l_name":l_name.get(),
        "address":address.get(),
        "city":city.get(),
        "state":state.get(),
        "zipcode":zipcode.get()
    })
    messagebox.showinfo("Addresses","Inserted successfully")
    conn.commit()
    conn.close()

    f_name.delete(0,END)
    l_name.delete(0,END)
    address.delete(0,END)
    city.delete(0,END)
    state.delete(0,END)
    zipcode.delete(0,END)

def query():
    conn= sqlite3.connect("address_book.db")
    c=conn.cursor()

    c.execute("SELECT *, oid from addresses")
    
    records=c.fetchall()
    print_record=""
    for record in records:
        print_record += str(record[0]) + ' ' + str(record[1]) + ' ' + '\t' + str(record[6]) + '\n'

    query=Label(root,text=print_record)
    query.grid(row=8,column=0,columnspan=2)
    conn.commit()
    conn.close()

def delete():
    conn=sqlite3.connect("address_book.db")
    c=conn.cursor()
    c.execute("DELETE from addresses WHERE oid =" + delete_box.get())
    print("Deleted sucessfully")
    delete_box.delete(0,END)
    conn.commit()
    conn.close()

def update():
    conn=sqlite3.connect("address_book.db")
    c=conn.cursor()
    recoed_id=delete_box.get()
    c.execute('''UPDATE addresses SET
    first_name= :first,
    last_name=:last,
    address=:address,
    city=:city,
    state=:state,
    zipcode=:zipcode
    WHERE oid=oid''',
    {'first':f_name_editor.get(),
    'last':l_name_editor.get(),
    'address':address_editor.get(),
    }
    )
def edit():
    global editor
    editor=Toplevel()
    editor.title("Update Data")
    editor.geometry('300x400')
    conn=sqlite3.connect("address_book.db")
    c=conn.cursor()
    record_id=delete_box.get()
    c.execute("SELECT * FROM addresses WHERE oid="+ record_id)
    records=c.fetchall()

    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor

    f_name_editor=Entry(editor,width=30)
    f_name_editor.grid(row=1,column=2)

    f_editor_label=Label(editor,text="First Name")
    f_editor_label.grid(row=1,column=1)

    l_name_editor=Entry(editor,width=30)
    l_name_editor.grid(row=2,column=2)

    l_editor_label=Label(editor,text="Last Name")
    l_editor_label.grid(row=2,column=1)

    address_editor=Entry(editor,width=30)
    address_editor.grid(row=3,column=2)

    a_editor_label=Label(editor,text="Address")
    a_editor_label.grid(row=3,column=1)

    city_editor=Entry(editor,width=30)
    city_editor.grid(row=4,column=2)

    c_editor_label=Label(editor,text="City")
    c_editor_label.grid(row=4,column=1)

    state_editor=Entry(editor,width=30)
    state_editor.grid(row=5,column=2)

    s_editor_label=Label(editor,text="State")
    s_editor_label.grid(row=5,column=1)

    zipcode_editor=Entry(editor,width=30)
    zipcode_editor.grid(row=6,column=2)

    z_editor_label=Label(editor,text="Zipcode")
    z_editor_label.grid(row=6,column=1)

    for record in records:
       f_name_editor.insert(0,record[0])
       l_name_editor.insert(0,record[1])
       address_editor.insert(0,record[2])
       city_editor.insert(0,record[3])
       state_editor.insert(0,record[4])
       zipcode_editor.insert(0,record[5])

    save_btn=Button(editor,text="Save")
    save_btn.grid(row=7,column=1,columnspan=2,pady=10,padx=10,ipadx=100,command=update)

f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root,width=30)
address.grid(row=2, column=1)

city = Entry(root,width=30)
city.grid(row=3, column=1)

state = Entry(root,width=30)
state.grid(row=4, column=1)

zipcode = Entry(root,width=30)
zipcode.grid(row=5, column=1)

delete_box=Entry(root,width=30)
delete_box.grid(row=9,column=1,pady=5)

f_name_label= Label(root, text="First Name")
f_name_label.grid(row=0, column=0)

l_name_label= Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

address_label= Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label= Label(root, text="City")
city_label.grid(row=3, column=0)

state_label= Label(root, text="State")
state_label.grid(row=4, column=0)

zipcode_label= Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

delete_id=Label(root,text="Delete ID")
delete_id.grid(row=9,column=0,pady=5)
submit_btn = Button(root,text="Add Records", command=submit)
submit_btn.grid(row=6,column=0, columnspan=2, pady=10,padx=10, ipadx=100)

query_button = Button(root, text="Show Records",command=query)
query_button.grid(row=7,column=0, columnspan=2, padx=10, pady=10, ipadx=100)

delete_btn=Button(root,text="Delete",command=delete)
delete_btn.grid(row=10,column=0,columnspan=3,pady=10,padx=10,ipadx=120)

update_btn=Button(root,text="Update",command=edit)
update_btn.grid(row=11,column=0,columnspan=2,pady=10,padx=10,ipadx=120)

conn.commit()
conn.close()


root.mainloop()

