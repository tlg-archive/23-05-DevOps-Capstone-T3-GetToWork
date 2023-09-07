import os
import json

#helper functions
def create_window():
    width = os.get_terminal_size().columns 
    print('~' * width)
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

# Classes for the Game (still in progress)
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
        #these print statements show the current room and exit options
        #print("current room",self.current_room)
        print("current exits",self.current_room.options)
        
        if action in self.current_room.options:
            self.current_room = self.current_room.options[action]
        else:
            print("You can't go that way.")

    #this function is currently used to display the current location description
    def look_around(self):
        create_window()
        print("\nCURRENT LOCATION: ", self.current_room.name)
        print("\n")
        print(self.current_room.description,"\n")
        create_window()

    #WILL WE NEED THIS FUNCTION?
    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"You take the {item_name}.")
                return
        print(f"There's no {item_name} here.")

    #WILL WE NEED THIS FUNCTION?
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

            #add the location names
            for index,loc_info in enumerate(locations_data["locations"]):
                location = Location(loc_info["name"], loc_info["description"])

                #add the location exits/options
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)

                #this grabs the items for the locations, this part of the function may need to be fixed later
                for item_name in loc_info["items"]:
                    #print(item_name)
                    item_info = self.load_item_data(items_file, item_name)
                    #print("info from the load item data function",item_info)
                    if item_info:
                        item = Item(item_name, item_info["description"])
                        #print("item name",item_name)
                        location.add_item(item_name)

                #set the location name
                self.locations[loc_info["name"]] = location

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
        print("Invalid command. Type 'Help' for more information.")

    def handle_take(self, noun):
        print(f"Handling TAKE command for {noun}")
        # Implement 'TAKE' logic here

    def handle_use(self, noun):
        print(f"Handling USE command for {noun}")
        # Implement 'USE' logic here
        self.player.move(noun)

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
        #sets the starting location of the game to be home
        starting_location = 'Home'
        self.player = Player("Player Name")
        self.player.current_room = self.locations[starting_location]
        #print("location names", list(self.locations.keys()))
        #print("exit options to next screen",list(self.locations))
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
            elif command in ["help", "info", "commands", "hint", "assist"]:
                print(game_text['help'])
            else:
                self.parse_command(command)

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

