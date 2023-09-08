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
    with open("json/items.json") as items_file:
        items_data = json.load(items_file)
        for item, details in items_data.items():
            if item == object_to_look.lower():
                print(details['description'])
                return

    for location, details in game.locations.items():
        if location.lower() == object_to_look.lower():
            print(details.description)
            return

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

    def move(self, noun):
        if noun.lower() in self.current_room.options:
            self.current_room = game.locations[noun]
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
        
            for loc_info in locations_data["locations"]:
                location = Location(loc_info["name"], loc_info["description"])
            
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)

                for item_name in loc_info.get("items", []):
                    item_info = self.load_item_data(items_file, item_name)
                    if item_info:
                        item = Item(item_name, item_info["description"])  # create an Item object
                        location.add_item(item)  # pass the Item object instead of string

                self.locations[loc_info["name"]] = location

 
    def handle_take(self, noun):
        print(f"Handling TAKE command for {noun}")
        self.player.take_item(noun)

    def handle_use(self, noun):
        print(f"Handling USE command for {noun}")
        self.player.move(noun.capitalize())

    def handle_drive(self, noun):
        print(f"Handling DRIVE command for {noun}")
        # Implement 'DRIVE' logic here
        self.player.move(noun.capitalize())

    def handle_board(self, noun):
        print(f"Handling BOARD command for {noun}")
        # Implement 'BOARD' logic here
        self.player.move(noun.capitalize())

    def handle_look(self, noun):
        print(f"Handling LOOK command for {noun}")
        if noun:
            display_description(noun)
        else:
            print("What do you want to look at?")

    def start_game(self):
        player_name = input("Enter your name: ")
        self.player = Player(player_name)
        self.player.current_room = self.locations["Home"]
        
        while True:
            self.player.look_around()
            command = input("> ").lower().split()
            verb = command[0]
            noun = ' '.join(command[1:]) if len(command) > 1 else None

            if verb == "look":
                self.handle_look(noun)
            elif verb == "take" or verb == "get":
                self.handle_take(noun)
            elif verb == "use":
                self.handle_use(noun)
            elif verb == "drive":
                self.handle_drive(noun)
            elif verb == "board":
                self.handle_board(noun)
            elif verb == "quit":
                break
            else:
                print("I'm not sure what you're trying to do.")

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

