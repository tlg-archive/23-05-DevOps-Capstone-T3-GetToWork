import os
import json
import random
import sys
import pygame 

#paths for file dependencies
script_dir = os.path.dirname(os.path.realpath(__file__))

title_file = os.path.join(script_dir, 'json', 'title.txt')
npc_file = os.path.join(script_dir, 'json', 'dialouge.json')
text_file = os.path.join(script_dir, 'json', 'game-text.json')
item_file = os.path.join(script_dir, 'json', 'items.json')
location_file = os.path.join(script_dir, 'json', 'Location.json')


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
    with open(text_file) as json_file:
        game_text = json.load(json_file)
    return game_text

def display_description(object_to_look):
    # Look in items
    with open(item_file) as items_file:
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
    def __init__(self, name, description,req_item,loc_delay):
        self.name = name
        self.description = description
        self.options = {}
        self.items = []
        self.required_item = req_item
        self.delay = loc_delay

    def add_option(self, action, loc):
        self.options[action] = loc

    """ def add_delay(self, action, loc):
        self.delay = loc_delay """

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

class Map:
    @staticmethod
    def show_map():
        with open("json/map.txt", "r") as file:
            map_list = file.readlines()
        print("Map:")
        for line in map_list:
            print(line)

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None
        self.current_time= 450

    def move(self, noun):
        #these print statements show the current room and exit options
        #print(noun, "noun")
        #print(f"current room: {self.current_room.name}") 
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
                    #self.advance_time()
                    random_room = random.sample(new_loc, 1)
                    self.current_room = game.locations[random_room[0]]
                    self.advance_time()
                else:
                    print(f"Oh no! You left your {self.current_room.required_item} at home. Please quit and restart to get this item.")
            else:
                new_loc = self.current_room.options.get(noun.lower())
                #grab a random location from the room options sub-array
                random_room = random.sample(new_loc, 1)

                #ACTUAL CODE TO UNCOMMENT BELOW WHEN THE ABOVE WORKS
                #self.advance_time()
                self.current_room = game.locations[random_room[0]]
                self.advance_time()
        else:
            print("You can't go that way.")

    def look_around(self):
        create_window()
        print(f"\n-----CURRENT LOCATION: {self.current_room.name}-----")
        #print("\n")
        #print(f"Time: {game.game_time}")
        #print(self.current_room.info())
        if hasattr(self.current_room, 'description'):
            print("\n")
            print(self.current_room.description,"\n")
           #self.display_status() 

            #Dynamically print all items in a room
            if len(self.current_room.items) > 0:
                print(f"-----ITEMS IN THIS ROOM-----")
                for item in self.current_room.items:
                    print(item.name)

            print("\n")
            self.display_status()
            #check for required item
            """ if self.current_room.required_item != "":
                print(f"required item: {self.current_room.required_item}")
            else:
                print("No required item for this room") """
        else:
            print(self.current_room.message,"\n")
            random_response = random.sample(self.current_room.random_response, 1)
            print(random_response[0], "\n")  
            self.display_status()
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
            print(game_text["empty"])
        else:
            print("Inventory:")
            for item in self.inventory:
                print(item.name)

    def talk_npc(self, noun):
        #THIS CODE SHOULD ONLY DISPLAY THE NPC DIALOGUE
        if noun.lower() in self.current_room.options:
            new_loc = self.current_room.options.get(noun.lower())
            #self.current_room = game.locations[new_loc]

            random_room = random.sample(new_loc, 1)
            #DELETE LATER
            #print(f"new loc = {new_loc}")
            #print(f"random room = {random_room}")
            self.current_room = game.locations[random_room[0]]
        else:
            print(f"You can't talk with {noun} here.")

    def advance_time(self, minutes=10):
        #print(f"current room for advance time troubleshooting: {self.current_room.name}")
        #print(f"current room delay: {self.current_room.delay}")
        if self.current_room.delay == 0:
            self.current_time +=  minutes
        else:
            self.current_time +=  self.current_room.delay
            print(f"YOU ARE DELAYED BY {self.current_room.delay} EXTRA MINUTES")
        if self.current_time >= 540:
            print(game_text['late'])
            sys.exit()

    def display_status(self):
        hours, minutes = divmod(self.current_time, 60)
        print("-----PLAYER STATUS-----")
        print(f'CURRENT TIME: {hours:02d}:{minutes:02d}am')
        self.inventory_list()

    def save_game(self, filename='save_game.json'):
        data = {
            'name': self.name,
            'inventory': [item.name for item in self.inventory],
            'current_room': self.current_room.name,
            'current_time': self.current_time
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    @classmethod    
    def load_game(cls, game, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        player = cls(data['name'])
        player.current_time = data['current_time']
        player.current_room = game.locations[data['current_room']]
        for item_name in data['inventory']:
            item_info = game.load_item_data(game.items_file, item_name)
            if item_info:
                item = Item(item_name, item_info["description"])
                player.inventory.append(item)
        return player


class Game:
    def __init__(self, locations_file, items_file, npc_file):
        self.locations = {}
        self.items = []
        self.npcs = {}
        self.player = None
        self.load_game_data(locations_file, items_file)
        self.load_npc(npc_file)
        #self.game_time= "7:30"
        self.items_file = items_file
        self.game_data = None
        self.is_new_game = True
        self.save_data = None


    def load_item_data(self, items_file, item_name):
        with open(items_file, "r") as items_file:
            items_data = json.load(items_file)
            return items_data.get(item_name)

    def load_game_data(self, locations_file, items_file):
        with open(locations_file, "r") as loc_file:
            locations_data = json.load(loc_file)
            for index, loc_info in enumerate(locations_data["locations"]):

                #create the location object
                location = Location(loc_info["name"], loc_info["description"],loc_info["required-item"],loc_info["delay"])
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)

                #adding items to the location items list
                for item_name in loc_info["items"]:
                    item_info = self.load_item_data(items_file, item_name)
                    if item_info:
                        item = Item(item_name, item_info["description"])
                        location.add_item(item)
                self.locations[loc_info["name"]] = location
    
    def handle_inventory(self):
        self.player.inventory_list()

    def load_npc(self,npc_file):
        with open(npc_file) as npc_file:
            npc_data = json.load(npc_file)
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

        if verb == 'save':
            self.save_game()
            print("Game saved!")
            return

        if verb == 'load':
            self.load_game()
            print("Game loaded!")
            return

        synonyms = {
            'take': ['take', 'grab', 'get', 'retrieve', 'snatch'],
            'use': ['use','drop'],
            'drive': ['drive','find'],
            'board': ['board', 'catch','stay','sit','ride', 'go','stay','head'],
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
        print(game_text["invalid"])

    def handle_take(self, noun):
        print(f"Handling TAKE command for {noun}")
        self.player.take_item(noun)

    def handle_use(self, noun):
        print(f"Handling USE command for {noun}")
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



    #IS THIS FUNCTION USED? ASK DEREK
    def increment_time(self):
        current_hour, current_minute = map(int, self.game_time.split(':'))
        current_minute += 10
        if current_minute >= 60:
            current_hour += 1
            current_minute -= 60

        self.game_time = f"{current_hour:02}:{current_minute:02}"
        if current_hour >= 24:
            self.game_time = "00:" + self.game_time.split(':')[1]

    def start_game(self):
        #print(f"Save data object {list(self.save_data.keys())}.")
        if self.is_new_game == True:
            starting_location = 'Home'
            self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            #test_loc = list(self.locations.keys())
            #print(f"List of locations {test_loc}")
        elif self.is_new_game == False:
            starting_location = self.save_data['current_room']
            self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]

            for item_name in self.save_data['inventory']:
                item_info = self.load_item_data(self.items_file, item_name)
                if item_info:
                    item = Item(item_name, item_info["description"])
                    self.player.inventory.append(item)

            self.player.current_time = self.save_data['current_time']
        
        while True:
            #FOR TROUBLESHOOTING, REMOVE LATER
            #print(f"current room options: {self.player.current_room.options}")

            #actual code
            self.player.look_around()
            command = input(">> ").strip().lower()
            if not command:
                continue
            if command == "quit":
                print(game_text['quit'])
                exit_command = input("> ").lower().strip()
                if exit_command in ['yes', 'exit', 'quit']:
                    clear_screen()
                    break
                elif exit_command in ['no']:
                    continue
            elif command in ["help", "info", "commands", "hint", "assist"]:
                print(game_text['help'])
            elif command in ["inventory", "pocket"]:
                self.handle_inventory()
            elif command == "time":
                self.player.display_status()
            elif command in ["map", "show map"]:
                game_map.show_map()
            else:
                self.parse_command(command)

    def save_game(self, filename='save_game.json'):
        data = {
            'name': self.player.name,
            'inventory': [item.name for item in self.player.inventory],
            'current_room': self.player.current_room.name,
            'current_time': self.player.current_time
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_game(self):
        with open('save_game.json', 'r') as f:
            data = json.load(f)
        self.is_new_game = False
        self.save_data = data
        print(data)
        
#SOUND FUNCTIONALITY BELOW
def sound():                
   sound_file_path = "json/soundtest.mp3"
   pygame.mixer.init()
   pygame.mixer.music.load(sound_file_path)
   pygame.mixer.music.play() 

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled

if __name__ == "__main__":
        clear_screen()
        pygame.mixer.init()
        sound()
    
while True:
        print_ascii(title_file)
        game_text = convert_json()
        print(game_text['intro'])
        print("Type 'Load' to load a saved game.")
        choice = input(">> ").strip().lower()

        if choice in ["start", "new game", "start new game"]:
            game = Game(location_file,item_file,npc_file)
            game.start_game()

        elif choice == "load":
            game = Game(location_file, item_file, npc_file)
            try:
                game.load_game()
                print("Game loaded!")
                game.start_game()
            except FileNotFoundError:
                print("No saved game found. Please start a new game.")

        elif choice in ["quit", "exit"]:
            print("Thanks for playing!")
            break
        else:
            print(game_text['error'])

