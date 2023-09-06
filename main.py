import os
import json

#Classes for the Game (still in progress)
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
        #self.load_game_data(locations_file, items_file)


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
                #sys.exit()
            else:
                print("Invalid command. Try 'go', 'look', 'take', 'inventory', or 'quit'.")


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