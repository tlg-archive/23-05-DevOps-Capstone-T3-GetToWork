import os
import json
import random

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

    def __str__(self):
        return self.name

class Location:
    def __init__(self, name, description,req_item):
        self.name = name
        self.description = description
        self.options = {}
        self.items = []
        self.required_item = req_item

    def add_option(self, action, loc):
        self.options[action] = loc

    def add_item(self, item):
        self.items.append(item)

    def add_req_item(self, item):
        self.required_item.append(item)

    def info(self):
        return f"name: {self.name}\ndescription: {self.description}\items:{self.items}\noptions:{self.options}"

class NPC:
    def __init__(self, name, message,req_item):
        self.name = name
        self.message = message
        self.random_response = []
        self.options = {}
        self.required_item = req_item

    def add_option(self, action, loc):
        self.options[action] = loc

    def info(self):
        return f"name: {self.name}\nmessage: {self.message}\nresponse:{self.random_response}\noptions:{self.options}"

    def add_req_item(self, item):
        self.required_item.append(item)

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None

    def move(self, noun):
        #these print statements show the current room and exit options
        #print(noun, "noun") 
        #print(f"current room options: {self.current_room.options}")
        #print(game.locations[noun])
        if noun.lower() in self.current_room.options:
            if self.current_room.required_item:
                #check your inventory to see if the required item exists, need to loop throught the inventory list
                check_req = False
                for item in self.inventory:
                    check_req = item.name == self.current_room.required_item
                    if check_req == True:
                        print("Leave the loop")
                        break

                if check_req == True:
                    new_loc = self.current_room.options.get(noun.lower())
                    self.current_room = game.locations[new_loc]
                else:
                    print(f"Oh no! You left your {self.current_room.required_item} at home. Please quit and restart to get this item.")
            else:
                new_loc = self.current_room.options.get(noun.lower())
                #print(f"Does this work? {self.current_room.options.get(noun.lower())}")
                self.current_room = game.locations[new_loc]
        else:
            print("You can't go that way.")

    def look_around(self):
        create_window()
        print("\nCURRENT LOCATION: ", self.current_room.name)
        print("\n")
        if hasattr(self.current_room, 'description'):
            print(self.current_room.description,"\n")

            #Dynamically print all items in a room
            if len(self.current_room.items) > 0:
                print(f"list of items in the current room:")
                for item in self.current_room.items:
                    print(item.name)

            #check for required item
            if self.current_room.required_item != "":
                print(f"required item: {self.current_room.required_item}")
            else:
                print("No required item for this room")
        else:
            print(self.current_room.message,"\n")
            random_response = random.sample(self.current_room.random_response, 1)
            print(random_response[0], "\n")  
        create_window()

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"You take the {item_name}.")
                return
        print(f"There's no {item_name} here.")

    def use_item(self, noun):
        #removes item from your inventory, adds it to the current location item list
        print(f"use item {noun}")
        #print(f"item list in room: {self.current_room.items}") #IS A CLASS/OBJECT LOOP THROUGH IT?
        if len(self.inventory) > 0: 
            for item in self.inventory:
                print(item, "item")
                print(self.inventory, "inventory") 
                if item.name == noun:
                    print("I WORK")
                    self.inventory.remove(item)
                    self.current_room.items.append(item)
                    print(f"You take used the {item.name} in {self.current_room}.")
        else:
            print("You have no items to use!")

    def inventory_list(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(item.name)

    def talk_npc(self, noun):
        #print(noun)
        #print("current room",self.current_room)
        #print(noun.title(), "noun") 
        #print("current room options", self.current_room.options)
        #print('game locations',game.locations)

        #THIS CODE SHOULD ONLY DISPLAY THE NPC DIALOGUE
        if noun.lower() in self.current_room.options:
            new_loc = self.current_room.options.get(noun.lower())
            self.current_room = game.locations[new_loc]
            #self.current_room = game.locations[noun.title()]
            #print(f"I WORK {noun}")
            """ with open("json/dialouge.json") as npc_file:
                npc_data = json.load(npc_file)
                for items in npc_data.items():
                    print(items) """
        else:
            print(f"You can't talk with {noun} here.")

class Game:
    def __init__(self, locations_file, items_file, npc_file):
        self.locations = {}
        self.items = []
        self.npcs = {}
        self.player = None
        self.load_game_data(locations_file, items_file)
        self.load_npc(npc_file)

    def load_item_data(self, items_file, item_name):
        with open(items_file, "r") as items_file:
            items_data = json.load(items_file)
            return items_data.get(item_name)

    def load_game_data(self, locations_file, items_file):
        with open(locations_file, "r") as loc_file:
            locations_data = json.load(loc_file)
            for index, loc_info in enumerate(locations_data["locations"]):
                location = Location(loc_info["name"], loc_info["description"],loc_info["required-item"])

                #add required item for the room
                #location.add_req_item(loc_info["required-item"])
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)
                for item_name in loc_info["items"]:
                    #print(f"item name: {item_name}")
                    item_info = self.load_item_data(items_file, item_name)
                    if item_info:
                        #print(f"adding item to location - item name: {item_name}")
                        item = Item(item_name, item_info["description"])
                        location.add_item(item)
                self.locations[loc_info["name"]] = location
    
    def handle_inventory(self):
        self.player.inventory_list()

    def load_npc(self,npc_file):
       #print("loading npc data")
        with open("json/dialouge.json") as npc_file:
            npc_data = json.load(npc_file)
            #self.locations[npc_name] = npc_name
            for npc_name, npc_info in npc_data.items():
                #create new NPC object
                new_npc = NPC(npc_name, npc_info["message"],npc_info["required-item"])
                new_npc.random_response = npc_info["random_response"]

                #add NPC dialogue exit options
                for opt_act, opt_dest in npc_info["options"].items():
                    new_npc.add_option(opt_act, opt_dest)
                self.locations[npc_name] = new_npc

    def parse_command(self, command):
        command_words = command.split(' ')
        verb = command_words[0]
        noun = ' '.join(command_words[1:]) if len(command_words) > 1 else None

        synonyms = {
            'take': ['take', 'grab', 'get', 'retrieve', 'snatch'],
            'use': ['use','drop'],
            'drive': ['drive'],
            'board': ['board', 'catch','stay','sit','ride', 'go','stay'],
            'look': ['look', 'examine', 'inspect', 'view', 'glance', 'scan', 'check', 'observe', 'see'],
            'talk': ['talk', 'speak', 'converse', 'chat', 'discuss', 'communicate'],
            'pull': ['pull', 'yank', 'tug', 'grab'],
            'buy': ['buy', 'purchase', 'acquire', 'obtain', 'get', 'secure'],
        }
        

        for key, values in synonyms.items():
            if verb in values:
                method_name= f"handle_{key}"
                method = getattr(self, method_name, None)

                if method and callable(method):
                    method(noun)
                    return
        print("Invaild command. Type 'Help' for more information.")

    def handle_take(self, noun):
        print(f"Handling TAKE command for {noun}")
        self.player.take_item(noun)

    def handle_use(self, noun):
        print(f"Handling USE command for {noun}")
        #self.player.move(noun.capitalize())
        self.player.use_item(noun)

    def handle_drive(self, noun):
        print(f"Handling DRIVE command for {noun}")
        # Implement 'DRIVE' logic here
        self.player.move(noun.title())

    def handle_board(self, noun):
        print(f"Handling BOARD command for {noun}")
        self.player.move(noun.title())

    def handle_pull(self, noun):
        print(f"Handling PULL command for {noun}")
        self.player.move(noun.title())

    def handle_look(self, noun):
        print(f"Handling LOOK command for {noun}")
        if noun:
            display_description(noun)
        else:
            print("What do you want to look at?")

    def handle_talk(self, noun):
        print(f"Handling TALK command for {noun}")
        # Implement 'TAKE' logic here
        self.player.talk_npc(noun)

    def handle_buy(self, noun):
        print(f"Handling BUY command for {noun}")
        # Implement 'TAKE' logic here
        self.player.talk_npc(noun)

    def start_game(self):
        starting_location = 'Home'
        self.player = Player("Player Name")
        self.player.current_room = self.locations[starting_location]
        test_loc = list(self.locations.keys())
        print(f"List of locations {test_loc}")
        
        while True:
            print(f"current room options: {self.player.current_room.options}")
            #actual code
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
            elif command in ["inventory", "pocket"]:
                self.handle_inventory()
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
            game = Game("json/Location.json","json/items.json","json/dialouge.json")
            game.start_game()
        elif choice in ["quit", "exit"]:
            print("Thanks for playing!")
            break
        else:
            print(game_text['error'])

