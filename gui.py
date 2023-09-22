from tkinter import *
from GetToWork import *
from PIL import Image, ImageTk

#tkinter.Tk(screenName="game", baseName=None, className='Tk', useTk=True, sync=False, use=None)
root = Tk()

image = Image.open("json/title2.png")
photo = ImageTk.PhotoImage(image)
root.title(photo)
my_label = Label(root, image=photo)                 
my_label.pack()


entry = Entry(root)
entry.pack()

button = Button(root ,text="Start")

button.pack()

root.mainloop()