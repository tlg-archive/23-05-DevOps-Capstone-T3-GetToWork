import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from GetToWork import convert_json

from app.game import Game
from app.label_printer import LabelPrinter

def hide_title(event, game_text):
    """Hide the title screen."""
    title.pack_forget()
    messagebox.showinfo("intro", game_text['intro'])

def show_help():
    """Display a help message."""
    messagebox.showinfo("Help", "This is a help message. Replace it with your actual help text.")

#tkinter.Tk(screenName="game", baseName=None, className='Tk', useTk=True, sync=False, use=None)
root = Tk()

image = Image.open("json/title2.png")
photo = ImageTk.PhotoImage(image)
root.title(photo)
title = Label(root, image=photo)
title.pack()

script_dir = os.path.dirname(os.path.abspath(__file__))
game = Game(script_dir)
game_text = convert_json(game.text_file)

entry = Entry(root)
entry.pack()

button = Button(root ,text="Start")
button.pack()
help_button = Button(root, text="Help", command=show_help)  # Bind the show_help function to the button
help_button.pack()

button.pack()

root.bind('<Return>', lambda event: hide_title(event, game_text))


root.mainloop()
