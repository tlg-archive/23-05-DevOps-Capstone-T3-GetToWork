import os
import json

# Helper functions
def create_window():
    width = os.get_terminal_size().columns 
    print('~' * width)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii(fn):
    with open(fn, 'r') as f:
        print(''.join([line for line in f]))

def convert_json():
    with open("json/game-text.json") as json_file:
        game_text = json.load(json_file)
    return game_text

def display_description(object_to_look):
    # Look in items
    with open("json/items.json") as items_file:
        items_data = json.load(items_file)
        for item, details in items_data.items():
            if item == object_to_look.lower():
                print(details['description'])
                return

    # Look in locations
    for location, details in game.locations.items():
        if location.lower() == object_to_look.lower():
            print(details.description)
            return

    # If the object_to_look isn't found
    print(f"Cannot find information about {object_to_look}.")

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.locations = []

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.options = {}
        self.items = []

    def add_option(self, action, loc):
        self.options[action] = loc

    def add_item(self, item):
        self.items.append(item)

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None

    def move(self, action):
        print("current exits",self.current_room.options)
        
        if action in self.current_room.options:
            self.current_room = self.current_room.options[action]
        else:
            print("You can't go that way.")

    def look_around(self):
        create_window()
        print("\nCURRENT LOCATION: ", self.current_room.name)
        print("\n")
        print(self.current_room.description,"\n")
        create_window()

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
    def __init__(self, locations_file, items_file):
        self.locations = {}
        self.items = []
        self.player = None
        self.load_game_data(locations_file, items_file)

    def load_item_data(self, items_file, item_name):
        with open(items_file, "r") as items_file:
            items_data = json.load(items_file)
            return items_data.get(item_name)

    def load_game_data(self, locations_file, items_file):
        with open(locations_file, "r") as loc_file:
            locations_data = json.load(loc_file)
            for index, loc_info in enumerate(locations_data["locations"]):
                location = Location(loc_info["name"], loc_info["description"])
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)
                for item_name in loc_info["items"]:
                    item_info = self.load_item_data(items_file, item_name)
                    if item_info:
                        item = Item(item_name, item_info["description"])
                        location.add_item(item_name)
                self.locations[loc_info["name"]] = location

    # Command handling functions
    # ... all your command handlers like handle_take, handle_use, etc. ...

    def handle_look(self, noun):
        if noun:
            display_description(noun)
        else:
            print("What do you want to look at?")

    def start_game(self):
        starting_location = 'Home'
        self.player = Player("Player Name")
        self.player.current_room = self.locations[starting_location]
        print(f"list of items in the current room {self.player.current_room.items}")
        while True:
            self.player.look_around()
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
            elif command in ["help", "options"]:
                print(game_text['help'])
            else:
                command_parts = command.split()
                if len(command_parts) == 1:
                    verb = command_parts[0]
                    if verb == "inventory":
                        self.player.inventory_list()
                    elif verb == "look":
                        self.handle_look(None)
                    else:
                        print(game_text['error'])
                else:
                    verb = command_parts[0]
                    noun = " ".join(command_parts[1:])
                    if verb == "look":
                        self.handle_look(noun)
                    # Add more command handlers like take, use, etc. as needed ...

if __name__ == "__main__":
    clear_screen()
    while True:
        print_ascii('json/title.txt')
        game_text = convert_json()
        print(game_text['intro'])
        choice = input(">> ").strip().lower()
        
        if choice in ["start", "new game", "start new game"]:
            game = Game("json/Location.json","json/items.json")
            game.start_game()
        elif choice in ["quit", "exit"]:
            print("Thanks for playing!")
            break
        else:
            print(game_text['error'])

