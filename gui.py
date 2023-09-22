from tkinter import *
from GetToWork import *
from PIL import Image, ImageTk

#tkinter.Tk(screenName="game", baseName=None, className='Tk', useTk=True, sync=False, use=None)
root = Tk()
#with open("json/title2.png", "r") as title:
#    title = title.read()
#    print(title)
image = Image.open("json/title2.png")
photo = ImageTk.PhotoImage(image)
root.title(photo)
my_label = Label(root, image=photo)

                 
my_label.pack()
root.mainloop()