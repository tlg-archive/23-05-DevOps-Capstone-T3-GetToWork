To create a simple console-based text adventure game in Python using classes, you can define classes for the different game components such as `Player`, `Room`, and `Item`. Here's a basic structure for such a game:

```python
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []

    def add_exit(self, direction, room):
        self.exits[direction] = room

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

    def look_around(self):
        print(self.current_room.description)

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

# Create items
key = Item("Key", "A rusty old key.")
book = Item("Book", "An old, dusty book with a leather cover.")

# Create rooms
start_room = Room("Start Room", "You are in a dimly lit room. There is a door to the north.")
living_room = Room("Living Room", "You are in a cozy living room with a fireplace.")

# Add exits to rooms
start_room.add_exit("north", living_room)
living_room.add_exit("south", start_room)

# Add items to rooms
start_room.add_item(key)
living_room.add_item(book)

# Create the player
player = Player("Player", start_room)

# Game loop
while True:
    player.look_around()
    command = input(">> ").strip().lower().split()

    if not command:
        continue

    if command[0] == "go" and len(command) > 1:
        player.move(command[1])
    elif command[0] == "look":
        player.look_around()
    elif command[0] == "take" and len(command) > 1:
        player.take_item(" ".join(command[1:]))
    elif command[0] == "inventory":
        player.inventory_list()
    elif command[0] == "quit":
        break
    else:
        print("Invalid command. Try 'go', 'look', 'take', 'inventory', or 'quit'.")
```

This code provides a basic structure for a text adventure game using classes for `Item`, `Room`, and `Player`. You can add more rooms, items, and game logic as needed to create a more extensive game.