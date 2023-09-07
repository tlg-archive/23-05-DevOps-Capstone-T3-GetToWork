import os
import json

# Classes for the Game (still in progress)
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []

    def add_exit(self, direction, Location):
        self.exits[direction] = Location

    def add_item(self, item):
        self.items.append(item)

class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.inventory = []
        self.current_room = current_room

    def move(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
        else:
            print("You can't go that way.")

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"You take the {item_name}.")
                return
        print(f"There's no {item_name} here.")

    def inventory_list(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(item.name)

class Game:
    def __init__(self):
        self.locations = {}
        self.items = []
        self.player = None

    def parse_command(self, command):
        command_words = command.split(' ')
        verb = command_words[0]
        noun = ' '.join(command_words[1:]) if len(command_words) > 1 else None
        
        synonyms = {
            'take': ['take', 'grab', 'get', 'retrieve', 'snatch'],
            'use': ['use'],
            'drive': ['drive', 'ride'],
            'board': ['board', 'catch'],
            'look': ['look', 'examine', 'inspect', 'view', 'glance', 'scan', 'check', 'observe', 'see'],
            'talk': ['talk', 'speak', 'converse', 'chat', 'discuss', 'communicate'],
            'pull': ['pull', 'yank', 'tug', 'grab'],
            'buy': ['buy', 'purchase', 'acquire', 'obtain', 'get', 'secure'],
        }
        
        for key, values in synonyms.items():
            if verb in values:
                method_name = f"handle_{key}"
                method = getattr(self, method_name, None)
                
                if method and callable(method):
                    method(noun)
                    return
        print("Invalid command.")

    def handle_take(self, noun):
        print(f"Handling TAKE command for {noun}")
        # Implement 'TAKE' logic here

    def handle_use(self, noun):
        print(f"Handling USE command for {noun}")
        # Implement 'USE' logic here

    def handle_drive(self, noun):
        print(f"Handling DRIVE command for {noun}")
        # Implement 'DRIVE' logic here

    def handle_board(self, noun):
        print(f"Handling BOARD command for {noun}")
        # Implement 'BOARD' logic here

    def handle_look(self, noun):
        print(f"Handling LOOK command for {noun}")
        # Implement 'LOOK' logic here

    def handle_talk(self, noun):
        print(f"Handling TALK command for {noun}")
        # Implement 'TALK' logic here

    def handle_pull(self, noun):
        print(f"Handling PULL command for {noun}")
        # Implement 'PULL' logic here

    def handle_buy(self, noun):
        print(f"Handling BUY command for {noun}")
        # Implement 'BUY' logic here

    def start_game(self):
        while True:
            print("GAME START")
            command = input(">> ").strip().lower()

            if not command:
                continue

            if command == "quit":
                print(game_text['quit'])
                exit_command = input("> ").lower().strip()
                if exit_command in ['yes', 'exit', 'quit']:
                    break
                elif exit_command in ['no']:
                    continue
            elif command in ["help", "info", "commands", "hint", "assist"]:
                print(game_text['help'])
            else:
                self.parse_command(command)

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'n' else 'clear')

def print_ascii(fn):
    f= open(fn,'r')
    print(''.join([line for line in f]))

def convert_json():
    #get general game text and convert to a Python Dict
    with open("json/game-text.json") as json_file:
	    game_text = json.load(json_file)
    return game_text
if __name__ == "__main__":
    clear_screen()
    while True:
        print_ascii('json/title.txt')
        game_text = convert_json()
        print(game_text['intro'])
        choice = input(">> ").strip()
        
        if choice in ["start", "new game", "start new game"]:
            game = Game()
            game.start_game()
        elif choice in ["quit", "exit"]:
            print("Thanks for playing!")
            break
        else:
            print(game_text['error'])
