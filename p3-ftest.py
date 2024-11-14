from tkinter import *
from tkinter import ttk
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Define a text widget with font-property
text= Text(win, height=15, font=('Noto Sans Mono',12,'bold'))
text.insert(INSERT, "Hey Folks!, Welcome to TutorialsPoint!")
text.insert(INSERT, "H e y  F o l k s ! ,  W e l c o m e  t o  T u t o r i a l s P o i n t !")
text.pack()
win.mainloop()
