import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from GetToWork import convert_json

from app.game import Game
from app.label_printer import LabelPrinter

def hide_title(event, game_text, game: Game, entry, button, root, title, title_text):
    """Hide the title screen."""
    title.pack_forget()
    title_text.pack_forget()
    game.start_game()
    root.unbind('<Return>')
    entry.pack()
    button.pack()
    scene = Label(root, text='')
    scene_printer = LabelPrinter(scene)
    messagebox.showinfo("intro", game_text['intro'])

def show_help():
    """Display a help message."""
    messagebox.showinfo("Help", "This is a help message. Replace it with your actual help text.")

def process_input(event, game, entry, game_text):
    pass

def main():
    root = Tk()

    image = Image.open("json/title2.png")
    photo = ImageTk.PhotoImage(image)
    root.title(photo)
    title = Label(root, image=photo)
    title.pack()
    title_text = Label(root, text="Press Enter to Start")
    title_text.pack()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    game = Game(script_dir)
    game_text = convert_json(game.text_file)
    sound_enabled = True
    sfx_enabled = True
    game.sound_manager.sound_enabled = sound_enabled
    game.sound_manager.sfx_enabled = sfx_enabled
    game.load_game_data()
    game.sound_manager.sound(game.bg_music_file, script_dir)

    button = Button(root ,text="Start")
    button.pack()
    help_button = Button(root, text="Help", command=show_help)  # Bind the show_help function to the button
    help_button.pack()

    button.pack()

    entry = Entry(root)
    button = Button(root ,text="Start")

    root.bind('<Return>', lambda event: hide_title(event, game_text, game, entry, button, root, title, title_text))

    root.mainloop()

if __name__ == "__main__":
    main()
