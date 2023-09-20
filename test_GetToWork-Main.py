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
item_sound_file = os.path.join(script_dir, 'sfx', 'get_item.mp3')
bg_music_file = os.path.join(script_dir, 'sfx', 'soundtest.mp3')
map_file = os.path.join(script_dir, 'json', 'map.txt')

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
    #print(f"Cannot find information about {object_to_look}.")
    item_err = game_text["no_find_item"].format(object_to_look=object_to_look)
    print(item_err)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.locations = []

    def __str__(self):
        return self.name

class Location:
    def __init__(self, name, description,req_item,loc_delay,map_key):
        self.name = name
        self.description = description
        self.options = {}
        self.items = []
        self.required_item = req_item
        self.delay = loc_delay
        self.map_key = map_key

    def add_option(self, action, loc):
        self.options[action] = loc
        print(f"loc options dict {self.options[action]}")
    def add_item(self, item):
        self.items.append(item)
        print(f"loc item list {item}")
    def add_req_item(self, item):
        self.required_item.append(item)
        print(f"loc req item list {self.required_item}")

    def info(self):
        return f"name: {self.name}\ndescription: {self.description}\items:{self.items}\noptions:{self.options}"

class NPC:
    def __init__(self, name, message,req_item,map_key):
        self.name = name
        self.message = message
        self.random_response = []
        self.options = {}
        self.required_item = req_item
        self.map_key = map_key

    def add_option(self, action, loc):
        self.options[action] = loc
        print(f"npc options list {self.options[action]}")

    def info(self):
        return f"name: {self.name}\nmessage: {self.message}\nresponse:{self.random_response}\noptions:{self.options}"

    def add_req_item(self, item):
        self.required_item.append(item)

class Map:
    def __init__(self):
        self.gen_map()
        self.map_list = self.gen_map()

    def gen_map(self):
        with open(map_file, "r") as file:
            map_list = file.readlines()
        return map_list

    def show_map(self):
        print(game_text["map_text"])
        for line in self.map_list:
            print(line)

    def update_map(self):
        self.map_list = self.gen_map()
        #get the map key from the current room
        current_key = game.player.current_room.map_key

        for index, line in enumerate(self.map_list):
            if current_key in line:
                try:
                    idx = line.index(game.player.current_room.name)
                except ValueError:
                    if "Bus Events" in line:
                        idx = line.index("Bus Events")
                    elif "Car Events" in line:
                        idx = line.index("Car Events")
                    else:
                        idx = line.index("Coffee Shop")
                updated_line = line[:idx] + ">> " + line[idx:]
                line = updated_line
                self.map_list[index] = updated_line
        
class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None
        self.current_time= 450


    def move(self, noun):
        if noun.lower() in self.current_room.options:
            required_item_loc = self.current_room.options.get(noun.lower())
            print(f"noun: {noun} cro: {self.current_room.options}")
            print(f"req item: {required_item_loc}")
            
            if game.locations[required_item_loc[0]].required_item:
                #check your inventory to see if the required item exists, need to loop throught the inventory list
                check_req = False
                for item in self.inventory:
                    check_req = item.name == game.locations[noun].required_item
                    if check_req == True:
                        break

                if check_req == True:
                    new_loc = self.current_room.options.get(noun.lower())
                    random_room = random.sample(new_loc, 1)
                    self.current_room = game.locations[random_room[0]]
                    self.advance_time()
                    self.play_sound(self.current_room.name)
                else:
                    item_err = game_text["no_item"].format(no_item=game.locations[noun].required_item)
                    print(item_err)
            else:
                new_loc = self.current_room.options.get(noun.lower())
                
                #grab a random location from the room options sub-array
                random_room = random.sample(new_loc, 1)

                self.current_room = game.locations[random_room[0]]
                self.advance_time()
                self.play_sound(self.current_room.name)
        else:
            print(game_text["no_move"])
            #print("You can't go that way.")

    def play_sound(self, new_location):
        global current_location
        current_location = self.current_room.name
        loc_sfx = game.location_music[new_location]

        if loc_sfx != "":
                #ONLY PLAY THE SOUND BELOW THE CURRENT ROOM HAS NOT CHANGED
                sound(loc_sfx)


    def look_around(self):
        create_window()
        #print(f"\n-----CURRENT LOCATION: {self.current_room.name}-----")

        item_err = game_text["current_location"].format(location=self.current_room.name)
        print(item_err)

        if hasattr(self.current_room, 'description'):
            print("\n")
            print(self.current_room.description,"\n")

            #Dynamically print all items in a room
            if len(self.current_room.items) > 0:
                #print(f"-----ITEMS IN THIS ROOM-----")
                print(game_text["items"])
                for item in self.current_room.items:
                    print(item.name)

            print("\n")
            self.display_status()
            game.game_map.update_map()
        else:
            print(self.current_room.message,"\n")
            random_response = random.sample(self.current_room.random_response, 1)
            print(random_response[0], "\n")  
            self.display_status()
            game.game_map.update_map()
        create_window()

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                #print(f"You take the {item_name}.")

                item_err = game_text["grab_item"].format(item_name=item_name)
                print(item_err)


                sfx_sound(item_sound_file)
                return
        #print(f"There's no {item_name} here.")

        item_err = game_text["item_none"].format(item_name=item_name)
        print(item_err)

    def use_item(self, noun):
        #removes item from your inventory, adds it to the current location item list
        if len(self.inventory) > 0: 
            for item in self.inventory:
                #print(item, "item")
                #print(self.inventory, "inventory") 
                if item.name == noun:
                    self.inventory.remove(item)
                    self.current_room.items.append(item)
                    #print(f"You take used the {item.name} in {self.current_room}.")
                    print(game_text["use_item"].format(item_name=item.name,current_room=self.current_room.name))
        else:
            #print("You have no items to use!")
            print(game_text["no_use"])

    def inventory_list(self):
        if not self.inventory:
            print(game_text["empty"])
        else:
            print(game_text["inventory"])
            for item in self.inventory:
                print(item.name)

    def talk_npc(self, noun):
        if noun.lower() in self.current_room.options:
            new_loc = self.current_room.options.get(noun.lower())

            random_room = random.sample(new_loc, 1)
            self.current_room = game.locations[random_room[0]]
        else:
            
            #print(f"You can't talk with {noun} here.")
            print(game_text["no_npc"].format(noun=noun))

    def advance_time(self, minutes=10):
        if self.current_room.delay == 0:
            self.current_time +=  minutes
        else:
            self.current_time +=  self.current_room.delay
            #print(f"YOU ARE DELAYED BY {self.current_room.delay} EXTRA MINUTES")
            #print(game_text["delay_mess"].format(delay=self.current_room.delay))
        if self.current_time > 540: #changed this from >= to allow for making it to DRW by 9 on the dot
            print(game_text['late'])
            sys.exit()

    def display_status(self):
        hours, minutes = divmod(self.current_time, 60)
        print(game_text["player_status"])
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
        self.location_music = {}
        self.items = []
        self.npcs = {}
        self.player = None
        self.load_game_data(locations_file, items_file)
        self.load_npc(npc_file)
        self.game_map = None
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
                location = Location(loc_info["name"], loc_info["description"],loc_info["required-item"],loc_info["delay"],loc_info["map-key"])
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)

                self.location_music[loc_info["name"]] = loc_info["sfx"]

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
                new_npc = NPC(npc_name, npc_info["message"],npc_info["required-item"],npc_info["map-key"])
                new_npc.random_response = npc_info["random_response"]

                #add NPC dialogue exit options
                for opt_act, opt_dest in npc_info["options"].items():
                    new_npc.add_option(opt_act, opt_dest)
                self.locations[npc_name] = new_npc

    def parse_command(self, command):
        command_words = command.split(' ')
        if len(command_words) == 1:
            print(game_text["need_noun"])
            return 
        verb = command_words[0]
        noun = ' '.join(command_words[1:]) if len(command_words) > 1 else None

        if verb == 'save':
            self.save_game()
            print(game_text["save_game"])
            return

        if verb == 'load':
            self.load_game()
            print(game_text["load_game"])
            return

        synonyms = {
            'take': ['take', 'grab', 'get', 'retrieve', 'snatch','pickup'],
            'use': ['use','drop'],
            'drive': ['drive','find'],
            'board': ['board', 'catch','stay','sit','ride', 'go','stay','head'],
            'look': ['look', 'examine', 'inspect', 'view', 'glance', 'scan', 'check', 'observe', 'see'],
            'talk': ['talk', 'speak', 'converse', 'chat', 'discuss', 'communicate', 'ask'],
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
        #print(f"Handling TAKE command for {noun}")
        self.player.take_item(noun)

    def handle_use(self, noun):
        #print(f"Handling USE command for {noun}")
        self.player.use_item(noun)

    def handle_drive(self, noun):
        #print(f"Handling DRIVE command for {noun}")
        # Implement 'DRIVE' logic here
        self.player.move(noun.title())

    def handle_board(self, noun):
        #print(f"Handling BOARD command for {noun}")
        self.player.move(noun.title())

    def handle_pull(self, noun):
        #print(f"Handling PULL command for {noun}")
        self.player.move(noun.title())

    def handle_look(self, noun):
        #print(f"Handling LOOK command for {noun}")
        if noun:
            display_description(noun)
        else:
            print(game_text["look"])

    def handle_talk(self, noun):
        #print(f"Handling TALK command for {noun}")
        # Implement 'TAKE' logic here
        self.player.talk_npc(noun)

    def handle_buy(self, noun):
        #print(f"Handling BUY command for {noun}")
        # Implement 'TAKE' logic here
        self.player.move(noun.title())

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
        if self.is_new_game == True:
            self.game_map = Map()
            starting_location = 'Home'
            self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            self.player.play_sound(starting_location)
        elif self.is_new_game == False:
            self.game_map = Map()
            starting_location = self.save_data['current_room']
            self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            self.player.play_sound(starting_location)

            for item_name in self.save_data['inventory']:
                item_info = self.load_item_data(self.items_file, item_name)
                if item_info:
                    item = Item(item_name, item_info["description"])
                    self.player.inventory.append(item)

            self.player.current_time = self.save_data['current_time']
        
        while True:
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
                self.game_map.show_map()
            elif command in ["toggle sound"]:
                toggle_sound()
                print("sound is", "on" if sound_enabled else "off")
            elif command == "volume up":
                volume_up()
                new_vol = round(current_volume * 100)
                print(game_text["vol_up"].format(current_volume=new_vol))
            elif command == "volume down":
                volume_down()
                new_vol = round(current_volume * 100)
                print(game_text["vol_down"].format(current_volume=new_vol))
            elif command == "sfx volume up":
                sfx_volume_up()
                sfx_vol = round(current_sfx_volume * 100)
                print(game_text["vol_up"].format(current_volume=sfx_vol))
            elif command == "sfx volume down":
                sfx_volume_down()
                sfx_vol = round(current_sfx_volume * 100)
                print(game_text["vol_up"].format(current_volume=sfx_vol))
            elif command == "toggle sfx":
                toggle_fx()
                print("sfx","on" if sfx_enabled else "off") 
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
        
#SOUND FUNCTIONALITY BELOW
pygame.mixer.init()
music_channel = pygame.mixer.Channel(0)
sfx_channel = pygame.mixer.Channel(1)

current_volume = 0.4
current_sfx_volume = 0.6

def sound(sound_file):
    #print(sound_file.split('/'))
    song_name_list = sound_file.split('/')
    array_len = len(song_name_list)

    script_dirs = os.path.dirname(os.path.realpath(__file__))
    sound_file_path = os.path.join(script_dirs, 'sfx', song_name_list[array_len-1])
    #print(f"sound file path: {sound_file_path}")
    #print(f"sound file: {sound_file}")           
    pygame.mixer.init()
    background_music = pygame.mixer.Sound(sound_file_path) #sound_file formerly
    music_channel.play(background_music, loops=-1)  # -1 loops indefinitely
    music_channel.set_volume(current_volume)

#PLAYS THE SOUND EFFECT SFX - USED IN Player.take_item()
def sfx_sound(sound_file):
    if not sfx_enabled:
        return
    sfx_music = pygame.mixer.Sound(sound_file)
    sfx_channel.play(sfx_music)  # -1 loops indefinitely
    sfx_channel.set_volume(current_sfx_volume)

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        music_channel.unpause()
    else:
        music_channel.pause() 

def toggle_fx():
    global sfx_enabled
    sfx_enabled = not sfx_enabled         
   
VOLUME_INCREMENT = 0.1
def volume_up():
    global current_volume
    current_volume += VOLUME_INCREMENT
    if current_volume > 1:
        current_volume = 1
    music_channel.set_volume(current_volume)

def volume_down():
    global current_volume
    current_volume -= VOLUME_INCREMENT
    if current_volume < 0:
        current_volume = 0
    music_channel.set_volume(current_volume)

def sfx_volume_up():
    global current_sfx_volume
    current_sfx_volume += VOLUME_INCREMENT
    if current_sfx_volume > 1:
        current_sfx_volume = 1
    sfx_channel.set_volume(current_volume)

def sfx_volume_down():
    global current_sfx_volume
    current_sfx_volume -= VOLUME_INCREMENT
    if current_sfx_volume < 0:
        current_sfx_volume = 0
    sfx_channel.set_volume(current_volume)


if __name__ == "__main__":
        clear_screen()
        sound_enabled = True
        sfx_enabled = True
    
while True:
        sound(bg_music_file)
        print_ascii(title_file)
        game_text = convert_json()
        print(game_text['intro'])
        choice = input(">> ").strip().lower()

        if choice in ["start", "new game", "start new game", "start game"]:
            game = Game(location_file,item_file,npc_file)
            game.start_game()

        elif choice in ["load", "load game"]:
            game = Game(location_file, item_file, npc_file)
            try:
                game.load_game()
                print(game_text["load_game"])
                game.start_game()
            except FileNotFoundError:
                print(game_text["no_save"])       

        elif choice in ["quit", "exit"]:
            print(game_text["thanks"])
            break
        else:
            print(game_text['error'])