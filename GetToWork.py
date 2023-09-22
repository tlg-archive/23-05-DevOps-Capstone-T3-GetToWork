import os
import json
import random
import sys
import pygame

from app.game import Game 

#paths for file dependencies

def print_ascii(file_name):
    with open(file_name, 'r') as f:
        print(''.join(list(f)))

def convert_json(text_file):
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    game = Game(script_dir)
    game.clear_screen()

    print(script_dir)
    sound_enabled = True
    sfx_enabled = True
    game.sound_manager.sound_enabled = sound_enabled
    game.sound_manager.sfx_enabled = sfx_enabled
    while True:
        game.sound_manager.sound(game.bg_music_file, script_dir)
        print_ascii(game.title_file)
        game_text = convert_json(game.text_file)
        print(game_text['intro'])
        choice = input(">> ").strip().lower()

        if choice in ["toggle sound"]:
            sound_enabled = not sound_enabled
            game.sound_manager.sound_enabled = sound_enabled

        if choice in ["toggle sfx"]:
            sfx_enabled = not sfx_enabled
            game.sound_manager.sfx_enabled = sfx_enabled

        if choice in ["start", "new game", "start new game", "start game"]:
            game = Game(script_dir)
            game.sound_manager.sound_enabled = sound_enabled
            game.sound_manager.sfx_enabled = sfx_enabled
            game.load_game_data()
            game.start_game(game_text)

        elif choice in ["load", "load game"]:
            game = Game(script_dir)
            game.sound_manager.sound_enabled = sound_enabled
            game.sound_manager.sfx_enabled = sfx_enabled
            game.load_game_data()
            try:
                game.load_game()
                print(game_text["load_game"])
                game.start_game(game_text)
            except FileNotFoundError:
                print(game_text["no_save"])

        elif choice in ["quit", "exit"]:
            print(game_text["thanks"])
            break
        else:
            print(game_text['error'])

if __name__ == "__main__":
    main()
