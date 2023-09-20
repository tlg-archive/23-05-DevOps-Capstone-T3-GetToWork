
import json
import os
from typing import Protocol
from app.item import Item
from app.location import Location
from app.map import Map
from app.npc import NPC
from app.player import Player
from app.sound_manager import SoundManager


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
        self.sound_manager = SoundManager()

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
    
    def handle_inventory(self, game_text: dict[str, str]):
        self.player.inventory_list(game_text)

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

    def parse_command(self, command, game_text: dict[str, str]):
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

    def handle_take(self, noun, item_sound_file: str, game_text: dict[str, str]):
        #print(f"Handling TAKE command for {noun}")
        self.player.take_item(noun, item_sound_file, game_text, self.sound_manager)

    def handle_use(self, noun, game_text: dict[str, str]):
        #print(f"Handling USE command for {noun}")
        self.player.use_item(noun, game_text)

    def handle_drive(self, noun, game_text: dict[str, str]):
        #print(f"Handling DRIVE command for {noun}")
        # Implement 'DRIVE' logic here
        self.player.move(noun.title(), self, game_text, self.sound_manager)

    def handle_board(self, noun, game_text: dict[str, str]):
        #print(f"Handling BOARD command for {noun}")
        self.player.move(noun.title(), self, game_text, self.sound_manager)

    def handle_pull(self, noun, game_text: dict[str, str]):
        #print(f"Handling PULL command for {noun}")
        self.player.move(noun.title(), self, game_text, self.sound_manager)

    def handle_look(self, noun, game_text: dict[str, str]):
        #print(f"Handling LOOK command for {noun}")
        if noun:
            display_description(noun)
        else:
            print(game_text["look"])

    def handle_talk(self, noun, game_text: dict[str, str]):
        #print(f"Handling TALK command for {noun}")
        # Implement 'TAKE' logic here
        self.player.talk_npc(noun, self, game_text)

    def handle_buy(self, noun, game_text: dict[str, str]):
        #print(f"Handling BUY command for {noun}")
        # Implement 'TAKE' logic here
        self.player.move(noun.title(), self, game_text, self.sound_manager)

    def increment_time(self):
        current_hour, current_minute = map(int, self.game_time.split(':'))
        current_minute += 10
        if current_minute >= 60:
            current_hour += 1
            current_minute -= 60

        self.game_time = f"{current_hour:02}:{current_minute:02}"
        if current_hour >= 24:
            self.game_time = "00:" + self.game_time.split(':')[1]

    def start_game(self, game_text: dict[str, str]):
        if self.is_new_game == True:
            self.game_map = Map()
            starting_location = 'Home'
            self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            self.player.play_sound(starting_location, self, self.sound_manager)
        elif self.is_new_game == False:
            self.game_map = Map()
            starting_location = self.save_data['current_room']
            self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            self.player.play_sound(starting_location, self, self.sound_manager)

            for item_name in self.save_data['inventory']:
                item_info = self.load_item_data(self.items_file, item_name)
                if item_info:
                    item = Item(item_name, item_info["description"])
                    self.player.inventory.append(item)

            self.player.current_time = self.save_data['current_time']
        
        while True:
            self.player.look_around(self, game_text)
            command = input(">> ").strip().lower()
            if not command:
                continue
            if command == "quit":
                print(game_text['quit'])
                exit_command = input("> ").lower().strip()
                if exit_command in ['yes', 'exit', 'quit']:
                    self.clear_screen()
                    break
                elif exit_command in ['no']:
                    continue
            elif command in ["help", "info", "commands", "hint", "assist"]:
                print(game_text['help'])
            elif command in ["inventory", "pocket"]:
                self.handle_inventory()
            elif command == "time":
                self.player.display_status(game_text)
            elif command in ["map", "show map"]:
                self.game_map.show_map(game_text)
            elif command in ["toggle sound"]:
                self.sound_manager.toggle_sound()
                print("sound is", "on" if self.sound_manager.sound_enabled else "off")
            elif command == "volume up":
                self.sound_manager.volume_up()
                new_vol = round(self.sound_manager.current_volume * 100)
                print(game_text["vol_up"].format(current_volume=new_vol))
            elif command == "volume down":
                self.sound_manager.volume_down()
                new_vol = round(self.sound_manager.current_volume * 100)
                print(game_text["vol_down"].format(current_volume=new_vol))
            elif command == "sfx volume up":
                self.sound_manager.sfx_volume_up()
                sfx_vol = round(self.sound_manager.current_sfx_volume * 100)
                print(game_text["vol_up"].format(current_volume=sfx_vol))
            elif command == "sfx volume down":
                self.sound_manager.sfx_volume_down()
                sfx_vol = round(self.sound_manager.current_sfx_volume * 100)
                print(game_text["vol_up"].format(current_volume=sfx_vol))
            elif command == "toggle sfx":
                self.sound_manager.toggle_fx()
                print("sfx","on" if self.sound_manager.sfx_enabled else "off") 
            else:
                self.parse_command(command, game_text)

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
        
    def create_window(self):
        width = os.get_terminal_size().columns 
        print('~' * width)
