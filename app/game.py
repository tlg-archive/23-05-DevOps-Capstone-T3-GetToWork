
import json
import os
from typing import Protocol
from app.item import Item
from app.location import Location
from app.map import Map
from app.npc import NPC
from app.player import Player
from app.printer_interface import Printer
from app.sound_manager import SoundManager


class Game:
    def __init__(self, script_dir: str):
        self.locations = {}
        self.location_music = {}
        self.items = []
        self.npcs = {}
        self.player = None
        self.game_map = None
        self.game_data = None
        self.is_new_game = True
        self.save_data = None
        self.sound_manager = SoundManager()
        self.game_time ='00:00'
        self.script_dir = script_dir
        self.title_file = os.path.join(script_dir, 'json', 'title.txt')
        self.npc_file = os.path.join(script_dir, 'json', 'dialouge.json')
        self.text_file = os.path.join(script_dir, 'json', 'game-text.json')
        self.item_file = os.path.join(script_dir, 'json', 'items.json')
        self.location_file = os.path.join(script_dir, 'json', 'Location.json')
        self.item_sound_file = os.path.join(script_dir, 'sfx', 'get_item.mp3')
        self.bg_music_file = os.path.join(script_dir, 'sfx', 'soundtest.mp3')
        self.map_file = os.path.join(script_dir, 'json', 'map.txt')
        self.load_npc()


    def load_item_data(self, item_name):
        with open(self.item_file, "r") as items_file:
            items_data = json.load(items_file)
            return items_data.get(item_name)

    def load_game_data(self):
        with open(self.location_file, "r") as loc_file:
            locations_data = json.load(loc_file)
            for index, loc_info in enumerate(locations_data["locations"]):

                #create the location object
                location = Location(loc_info["name"], loc_info["description"],loc_info["required-item"],loc_info["delay"],loc_info["map-key"])
                for opt_act, opt_dest in loc_info["options"].items():
                    location.add_option(opt_act, opt_dest)

                self.location_music[loc_info["name"]] = loc_info["sfx"]

                #adding items to the location items list
                for item_name in loc_info["items"]:
                    item_info = self.load_item_data(item_name)
                    if item_info:
                        item = Item(item_name, item_info["description"])
                        location.add_item(item)
                self.locations[loc_info["name"]] = location
    
    def handle_inventory(self, game_text: dict[str, str]):
        self.player.inventory_list(game_text)

    def load_npc(self):
        try:
            with open(self.npc_file) as npc_file:
                npc_data = json.load(npc_file)
                for npc_name, npc_info in npc_data.items():
                    #create new NPC object
                    new_npc = NPC(npc_name, npc_info["message"],npc_info["required-item"],npc_info["map-key"])
                    new_npc.random_response = npc_info["random_response"]

                    #add NPC dialogue exit options
                    for opt_act, opt_dest in npc_info["options"].items():
                        new_npc.add_option(opt_act, opt_dest)
                    self.locations[npc_name] = new_npc
        except FileNotFoundError as err:
            print(err)

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
            'take': ['take', 'grab', 'get', 'retrieve', 'snatch','pickup', 'buy', 'purchase', 'acquire', 'obtain', 'get', 'secure'],
            'use': ['use','drop', 'pull', 'yank', 'tug', 'grab'],
            'move': ['board', "move", 'catch','stay','sit','ride', 'go','stay','head', 'drive','find'],
            'look': ['look', 'examine', 'inspect', 'view', 'glance', 'scan', 'check', 'observe', 'see'],
            'talk': ['talk', 'speak', 'converse', 'chat', 'discuss', 'communicate', 'ask']
        }
        
        for key, values in synonyms.items():
            if verb in values:
                method_name= f"handle_{key}"
                methods = {
                    'handle_take': {'method': self.handle_take, 'args': [noun, self.item_sound_file, game_text]},
                    'handle_use': {'method': self.handle_use, 'args': [noun, game_text]},
                    'handle_move': {'method': self.handle_move, 'args': [noun, game_text]},
                    'handle_look': {'method': self.handle_look, 'args': [noun, game_text]},
                    'handle_talk': {'method': self.handle_talk, 'args': [noun, game_text]},
                }
                call = methods.get(method_name, None)

                if call and callable(call['method']):
                    call['method'](*call['args'])
                    return
        print(game_text["invalid"])

    def handle_take(self, noun, item_sound_file: str, game_text: dict[str, str]):
        #print(f"Handling TAKE command for {noun}")
        self.player.take_item(noun, item_sound_file, game_text, self.sound_manager)
        self.player.move(noun.title(), self, game_text, self.sound_manager)

    def handle_use(self, noun, game_text: dict[str, str]):
        #print(f"Handling USE command for {noun}")
        self.player.use_item(noun, game_text)
        self.player.move(noun.title(), self, game_text, self.sound_manager)
    
    def handle_move(self, noun, game_text: dict[str, str]):
        #print(f"Handling DRIVE command for {noun}")
        # Implement 'DRIVE' logic here
        self.player.move(noun.title(), self, game_text, self.sound_manager)

    def handle_look(self, noun, game_text: dict[str, str]):
        #print(f"Handling LOOK command for {noun}")
        if noun:
            self.display_description(noun, game_text)
        else:
            print(game_text["look"])

    def handle_talk(self, noun, game_text: dict[str, str]):
        #print(f"Handling TALK command for {noun}")
        # Implement 'TAKE' logic here
        self.player.talk_npc(noun, self, game_text)


    def increment_time(self):
        current_hour, current_minute = map(int, self.game_time.split(':'))
        current_minute += 10
        if current_minute >= 60:
            current_hour += 1
            current_minute -= 60

        self.game_time = f"{current_hour:02}:{current_minute:02}"
        if current_hour >= 24:
            self.game_time = "00:" + self.game_time.split(':')[1]

    def parse_command(self, game_text: dict[str, str], printer: Printer, debug: bool = False, iterations_limit: int = 1):
            self.player.look_around(self.get_self(), game_text)
            command = input(">> ").strip().lower()
            self.clear_screen()
            if not command:
                return 
            if command == "quit":
                printer.print(game_text['quit'])
                printer.update()
                exit_command = input("> ").lower().strip()
                if exit_command in ['yes', 'exit', 'quit']:
                    self.clear_screen()
                    quit()
                elif exit_command in ['no']:
                    printer.print(exit_command)
                    return
            elif command in ["help", "info", "commands", "hint", "assist"]:
                printer.print(game_text['help'])
                printer.update()
            elif command in ["inventory", "pocket"]:
                self.handle_inventory(game_text)
            elif command == "time":
                self.player.display_status(game_text)
            elif command in ["map", "show map"]:
                self.game_map.show_map(game_text)
            elif command in ["toggle sound"]:
                self.sound_manager.toggle_sound()
                printer.print("sound is", "on" if self.sound_manager.sound_enabled else "off")
            elif command == "volume up":
                self.sound_manager.volume_up()
                new_vol = round(self.sound_manager.current_volume * 100)
                printer.print(game_text["vol_up"].format(current_volume=new_vol))
            elif command == "volume down":
                self.sound_manager.volume_down()
                new_vol = round(self.sound_manager.current_volume * 100)
                printer.print(game_text["vol_down"].format(current_volume=new_vol))
            elif command == "sfx volume up":
                self.sound_manager.sfx_volume_up()
                sfx_vol = round(self.sound_manager.current_sfx_volume * 100)
                printer.print(game_text["sfx_up"].format(current_volume=sfx_vol))
            elif command == "sfx volume down":
                self.sound_manager.sfx_volume_down()
                sfx_vol = round(self.sound_manager.current_sfx_volume * 100)
                printer.print(game_text["sfx_down"].format(current_volume=sfx_vol))
            elif command == "toggle sfx":
                self.sound_manager.toggle_fx()
                printer.print("sfx","on" if self.sound_manager.sfx_enabled else "off")
            else:
                self.parse_command(command, game_text)

    def start_game(self, debug: bool = False):
        if self.is_new_game == True:
            self.game_map = Map(self.map_file)
            starting_location = 'Home'
            if not debug:
                self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            self.player.play_sound(starting_location, self, self.sound_manager)
        elif self.is_new_game == False:
            self.game_map = Map(self.map_file)
            starting_location = self.save_data['current_room']
            if not debug:
                self.player = Player("Player Name")
            self.player.current_room = self.locations[starting_location]
            self.player.play_sound(starting_location, self, self.sound_manager)

            for item_name in self.save_data['inventory']:
                item_info = self.load_item_data(item_name)
                if item_info:
                    item = Item(item_name, item_info["description"])
                    self.player.inventory.append(item)

            self.player.current_time = self.save_data['current_time']

    def save_game(self, filename='save_game.json'):
        data = {
            'name': self.player.name,
            'inventory': [item.name for item in self.player.inventory],
            'current_room': self.player.current_room.name,
            'current_time': self.player.current_time
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_game(self, filename='save_game.json'):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.is_new_game = False
        self.save_data = data
        
    def create_window(self, printer: Printer, width: int):
        printer.print('~' * width)


    def clear_screen(self, printer: Printer):
        printer.clear()
        printer.update()


    def display_description(self, object_to_look, game_text: dict[str, str], printer: Printer):
        # Look in items
        with open(self.item_file) as items_file:
            items_data = json.load(items_file)
            for item, details in items_data.items():
                if item == object_to_look.lower():
                    printer.print(details['description'])
                    printer.update()
                    return

        # Look in locations
        for location, details in self.locations.items():
            if location.lower() == object_to_look.lower():
                printer.print(details.description)
                printer.update()
                return

        # If the object_to_look isn't found
        #print(f"Cannot find information about {object_to_look}.")
        item_err = game_text["no_find_item"].format(object_to_look=object_to_look)
        printer.print(item_err)
        printer.update()

    def get_self(self):
        return self
