import os

#Classes for the Game (still in progress)
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

class Game:
    def __init__(self):
        self.locations = {}
        self.items = []
        self.player = None
        #self.load_game_data(locations_file, items_file)


    def start_game(self):
        while True:
            print("GAME START")
            command = input(">> ").strip().lower()

            if not command:
                continue

            if command == "quit":
                print("YOU ARE QUITTING THE GAME TO THE TITLE SCREEN. WRITE MORE CODE HERE")
                break
                #sys.exit()
            else:
                print("Invalid command. Try 'go', 'look', 'take', 'inventory', or 'quit'.")


def clear_screen():
    os.system('cls' if os.name == 'n' else 'clear')

game_intro = """Good morning! You just moved to Chicago to start your new career as a DevOps Specialist with DRW. Today's your first day in the office but you're not used to commute in the city!\n\nLet's see if you can make it to work on time, or be late on your very first day!"""

if __name__ == "__main__":
    clear_screen()
    while True:
        print("GET TO WORK")
        print(game_intro)
        choice = input("\nStart New Game\nQuit\n>> ").strip()
        
        if choice in ["start", "new game", "start new game"]:
            game = Game()
            game.start_game()
        elif choice in ["quit", "exit"]:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter one of the the commands below to progress.")