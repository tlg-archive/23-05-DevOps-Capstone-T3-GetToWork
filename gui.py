from tkinter import *
from GetToWork import *
from PIL import Image, ImageTk

def hide_title(event):
    """Hide the title screen."""
    title.pack_forget()

#tkinter.Tk(screenName="game", baseName=None, className='Tk', useTk=True, sync=False, use=None)
root = Tk()

image = Image.open("json/title2.png")
photo = ImageTk.PhotoImage(image)
root.title(photo)
title = Label(root, image=photo)
title.pack()


entry = Entry(root)
entry.pack()

button = Button(root ,text="Start")
button.pack()

root.bind('<Return>', hide_title)

root.mainloop()
