import os
from tkinter import END, Button, Entry, Label, Tk, messagebox
from tkinter import *
from GetToWork import convert_json

from app.game import Game
from app.label_printer import LabelPrinter
from app.popup_window import PopupWindow

def hide_title(event, game_text: dict[str, str], game: Game, entry: Entry, root, title, title_text):
    """Hide the title screen."""
    title.pack_forget()
    title_text.pack_forget()
    game.start_game()
    root.unbind('<Return>')
    
    paned_window = PanedWindow(root , orient='vertical', background= "black", border=5)
    paned_window.pack()
    debug_text = Label(root, text="Debug Text", height= 2)
    debug_text.pack(side=TOP)
    paned_window.add(debug_text)
    debug_printer = LabelPrinter(debug_text)
    scene_text = Label(root, text='', height=30)
    scene_text.pack(side=TOP)
    paned_window.add(scene_text)
    scene_printer = LabelPrinter(scene_text)
    status_text = Label(root, text='', height=4)
    status_text.pack(side=TOP)
    paned_window.add(status_text)
    status_printer = LabelPrinter(status_text)
    result_text = Label(root, text='', height=3)
    result_text.pack(side=BOTTOM)
    result_printer = LabelPrinter(result_text)
    paned_window.add(result_text)
    entry.pack()
    game.status_printer = status_printer
    game.scene_printer = scene_printer
    game.debug_printer = debug_printer
    game.result_printer = result_printer
    game.show_location(game_text)
    game.scene_printer.update()
    root.bind('<Return>', lambda event: process_input(event, game, entry, game_text))
    messagebox.showinfo("intro", game_text['intro'])

def show_help():
    """Display a help message."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open('/'.join([script_dir, 'json/help.txt']), "r") as help_file:
        text = help_file.read()
        messagebox.showinfo("Help", text)

def process_input(event, game: Game, entry: Entry, game_text: dict[str, str]):
    """Process the player's input."""
    player_input = entry.get()
    entry.delete(0, END)
    game.clear_screen()
    game.parse_input(game_text, player_input)
    game.show_location(game_text)
    game.debug_printer.update()
    game.scene_printer.update()
    game.result_printer.update()



def main():
    root = Tk(sync=True, screenName="Get To Work")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open('/'.join([script_dir, 'json/title.txt']), 'r') as f:
        title_ = f.read()
    title = Label(root, text=title_, font=("Courier", 20), foreground="white", background="black")
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

    help_button = Button(root, text="Help", command=show_help)
    help_button.pack()
    popup_manager = PopupWindow(root)
    entry = Entry(root)
    button = Button(root, text="Options", command=lambda: popup_manager.create_popup_window(game))
    button.pack()

    root.bind('<Return>', lambda event: hide_title(event, game_text, game, entry, root, title, title_text))

    root.mainloop()

if __name__ == "__main__":
    main()