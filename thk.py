from tkinter import *
import os
import glob

file_paths=[]
os.chdir("./")


file_paths = tuple(file_paths)

#functions
def show_values():
    ct = 1
    for i in listbox1.curselection():
        print(listbox1.get(i))
def on_select():
    ct = 1
    print(listbox1.get(listbox1.curselection()[0]))
    for file in glob.glob(f"./dcm_exports/{listbox1.get(listbox1.curselection()[0])}/*.dcm"):
        fp = file.split("\\")
        listbox2.insert(ct,fp[1])
        ct+=1
        print(file)

master = Tk()
master.geometry('400x300')
# Nesneler
w1 = Scale(master, from_=0, to=1000, orient=HORIZONTAL)
w2 = Scale(master, from_=0, to=1000 , orient=HORIZONTAL)
bt = Button(master, text='Show', command=show_values,width=10)
bt_list_c = Button(master, text='Dosya değiştir', command=on_select,width=10)
namelbl = Label(master, text="Name")
listbox1 = Listbox(
    master,
    listvariable=file_paths,
    height=8,
    selectmode='single')
ct = 1
for dir in os.listdir("./dcm_exports/./"):
    listbox1.insert(ct,dir)
    ct+=1
listbox2 = Listbox(
    master,
    listvariable=file_paths,
    height=8,
    selectmode='single')

#grid
w1.set(118)
w1.grid(column=0,row=0,padx=10,pady=5,sticky=W)
w2.set(162)
w2.grid(column=0,row=1,padx=10,pady=2,sticky=W)

listbox1.grid(column=3,row=1,padx=30,pady=5,columnspan=2)
listbox2.grid(column=5,row=1,pady=5)

bt.grid(column=5,row=5,padx=10,pady=5)
bt_list_c.grid(column=3,row=5,padx=10,pady=5)
namelbl.grid(column=3,row=0,padx=5,pady=5)


master.mainloop()

