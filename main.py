#Classes for the Game (still in progress)
import os
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


## Create items, grabbing information from the JSON file
## Create rooms
## Add exits to rooms


#Setup code

#Title screen code - Demetra Ticket
def clear_screen():
    os.system('cls' if os.name == 'n' else 'clear')
def show_game_title():   
    clear_screen()
    print("GET TO WORK")
show_game_title()   

#Game information code - Cayla ticket
