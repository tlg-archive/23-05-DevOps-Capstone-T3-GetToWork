        
import json
import os
import random
import sys
from typing import Protocol
from app.item import Item
from app.printer_interface import Printer
from app.sound_manager import SoundManager

class Location(Protocol):
    name: str
    required_item: str
    delay: int
    options: dict[str, str]
    items: list[Item]
    message: str
    random_response: list[str]

class Map(Protocol):
    def update_map(self, game):
        pass

class Game(Protocol):
    locations: dict[str, Location]  # Add the required attributes
    location_music: dict[str, str]  # Add the required attributes
    items_file: str  # Add the required attributes
    game_map: Map  # Add the required attributes

    def load_item_data(self, items_file: str, item_name: str) -> dict:
        with open(items_file, 'r') as f:
            items = json.load(f)
        return items.get(item_name)

    def create_window(self):
        width = os.get_terminal_size().columns 
        print('~' * width)



class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_room = None
        self.current_time = 450


    def move(self, noun, game: Game, game_text: dict[str, str], sound_manager: SoundManager):
        if noun.lower() in self.current_room.options:
            possible_locations = self.current_room.options.get(noun.lower())
            if game.locations[possible_locations[0]].required_item:
                item_names = [item.name.lower() for item in self.inventory]
                if game.locations[noun].required_item.lower() in item_names:
                    random_room = random.sample(possible_locations, 1)
                    self.current_room = game.locations[random_room[0]]
                    self.advance_time(game_text)
                    self.play_sound(self.current_room.name, game, sound_manager)
                else:
                    return game_text["no_item"].format(no_item=game.locations[noun].required_item)
            else:
                new_loc = self.current_room.options.get(noun.lower())
                random_room = random.sample(new_loc, 1)

                self.current_room = game.locations[random_room[0]]
                self.advance_time(game_text)
                self.play_sound(self.current_room.name, game, sound_manager)
        else:
            return game_text["no_move"]
            #print("You can't go that way.")

    def play_sound(self, new_location, game, sound_manager: SoundManager):
        loc_sfx = game.location_music[new_location]

        if loc_sfx != "":
                #ONLY PLAY THE SOUND BELOW THE CURRENT ROOM HAS NOT CHANGED
                sound_manager.sound(loc_sfx, game.script_dir)


    def look_around(self, game: Game, game_text: dict[str, str]):
        #game.create_window()
        #print(f"\n-----CURRENT LOCATION: {self.current_room.name}-----")
        result = ''
        result += self.current_room.name + "\n"
        result += game_text["current_location"].format(location=self.current_room.name) + "\n"

        if hasattr(self.current_room, 'description'):
            result += "\n"
            result += self.current_room.description + "\n"

            #Dynamically print all items in a room
            if len(self.current_room.items) > 0:
                #print(f"-----ITEMS IN THIS ROOM-----")
                result += game_text["items"] + "\n"
                for item in self.current_room.items:
                    result += item.name + "\n"

            result += "\n"
            self.display_status(game_text)
            game.game_map.update_map(game)
        else:
            result += self.current_room.message + "\n"
            random_response = random.sample(self.current_room.random_response, 1)
            result += random_response[0] + "\n"
            self.display_status(game_text)
            game.game_map.update_map(game)

        return result

    def take_item(self, item_name, item_sound_file, game_text: dict[str, str], sound_manager: SoundManager):
        result = ''
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                #print(f"You take the {item_name}.")

                result += game_text["grab_item"].format(item_name=item_name) + "\n"

                sound_manager.sfx_sound(item_sound_file)
                return result
        #print(f"There's no {item_name} here.")

        result += game_text["item_none"].format(item_name=item_name)
        return result

    def use_item(self, noun, game_text: dict[str, str]):
        result = ''
        #removes item from your inventory, adds it to the current location item list
        if len(self.inventory) > 0 and noun in [item.name for item in self.inventory]: 
            item = [item for item in self.inventory if item.name == noun][0]
            self.inventory.remove(item)
            self.current_room.items.append(item)
            #print(f"You take used the {item.name} in {self.current_room}.")
            result += game_text["use_item"].format(item_name=item.name,current_room=self.current_room.name) + "\n"
        else:
            #print("You have no items to use!")
            result += game_text["no_use"]
        return result

    def inventory_list(self, game_text: dict[str, str]):
        result = ''
        if not self.inventory:
            result += game_text["empty"]
        else:
            result += game_text["inventory"] + "\n"
            for item in self.inventory:
                result += item.name + "\n"
        return result

    def talk_npc(self, noun, game: Game, game_text: dict[str, str]):
        if noun.lower() in self.current_room.options:
            new_loc = self.current_room.options.get(noun.lower())

            random_room = random.sample(new_loc, 1)
            self.current_room = game.locations[random_room[0]]
            return self.current_room.message
        else:
            return game_text["no_npc"].format(noun=noun)

    def advance_time(self, game_text: dict[str, str], minutes=10, printer: Printer = None):
        if self.current_room.delay == 0:
            self.current_time +=  minutes
        else:
            self.current_time +=  self.current_room.delay
            #print(f"YOU ARE DELAYED BY {self.current_room.delay} EXTRA MINUTES")
            #print(game_text["delay_mess"].format(delay=self.current_room.delay))
        if self.current_time > 540: #changed this from >= to allow for making it to DRW by 9 on the dot
            printer.print(game_text['late'])
            printer.update()
            quit(0)

    def display_status(self, game_text: dict[str, str]):
        result = ''
        hours, minutes = divmod(self.current_time, 60)
        result += game_text["player_status"] + "\n"
        result += f'CURRENT TIME: {hours:02d}:{minutes:02d}am' + "\n"
        result += self.inventory_list(game_text)
        return result

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