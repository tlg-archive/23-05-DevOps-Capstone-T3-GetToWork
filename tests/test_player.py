import json
import os
from unittest.mock import MagicMock
import pytest
from app.player import Game, Player, Location, Map
from app.sound_manager import SoundManager
from app.item import Item

# Define test fixtures
@pytest.fixture
def player():
    return Player("Test Player")

@pytest.fixture
def saved_game_filename(tmp_path):
    # Create a temporary directory and return the path to a saved game file
    return os.path.realpath("tests/test_save.json")

@pytest.fixture
def load_game_filename(tmp_path):
    # Create a temporary directory and return the path to a saved game file
    return os.path.realpath("tests/test_load.json")



# Define a fixture to load the game_text JSON file
@pytest.fixture
def game_text():
    with open(os.path.realpath("json/game-text.json"), "r") as file:  # Replace with the actual path to your game_text.json
        return json.load(file)


@pytest.fixture
def items():
    result_items = {}
    with open(os.path.realpath("./tests/test_items.json"), 'r') as f:
        items = json.load(f)
    for item in items.keys():
        result_items[item] = Item(items[item]['name'], items[item]['description'])
    return result_items

@pytest.fixture
def locations(items):
    result = {}
    with open(os.path.realpath("./tests/test_npcs.json"), 'r') as f:
        npcs = json.load(f)
    for npc in npcs.keys():
        npc_obj = MagicMock(spec=Location)
        npc_obj.name = npc
        npc_obj.options = npcs[npc].get("options")
        required_item = npcs[npc].get("required-item")
        if required_item in items:
            npc_obj.required_item = items[required_item]
        npc_obj.map_key = npcs[npc].get("map_key")
        npc_obj.message = npcs[npc].get("message")
        npc_obj.random_response = npcs[npc].get("random_response")
        result[npc] = npc_obj

    with open(os.path.realpath("./tests/test_locations.json"), 'r') as f:
        locations = json.load(f)
    for location in locations:
        resulting_location = MagicMock(spec=Location)
        resulting_location.name = location.get("name")
        resulting_location.description = location.get("description")
        resulting_location.options = location.get("options")
        resulting_location.items = []
        for item in location.get("items", []):
            if item in items:
                resulting_location.items.append(items[item])
        required_item = location.get("required-item")
        if required_item in items:
            resulting_location.required_item = required_item
        else:
            resulting_location.required_item = None
        resulting_location.delay = location.get("delay")
        resulting_location.map_key = location.get("map_key")
        resulting_location.message = location.get("message")
        resulting_location.random_response = location.get("random_response")
        resulting_location.sfx = location.get("sfx")
        result[resulting_location.name] = resulting_location
    return result

@pytest.fixture
def game(locations):
    game: Game = MagicMock(spec=Game)
    game.script_dir = os.path.realpath("./tests")
    game.locations = locations
    game.location_music = {location.name: location.sfx for location in locations.values() if hasattr(location, "sfx")}
    game.items_file = os.path.realpath("./tests/test_items.json")
    game.game_map: Map = MagicMock(spec=Map)
    return game

@pytest.fixture
def sound_manager():
    soundManager: SoundManager = MagicMock(spec=SoundManager)
    return soundManager

# Define test cases
def test_player_initialization(player):
    assert player.name == "Test Player"
    assert player.inventory == []
    assert player.current_room is None
    assert player.current_time == 450

def test_move_valid_noun(player, game, sound_manager, game_text):
    # Mock the game object
    player.current_room = game.locations["room_a"]
    assert player.current_room.name == game.locations["room_a"].name

    player.move("room_c", game, game_text, sound_manager)
    assert player.current_room.name == game.locations["room_c"].name

def test_move_valid_with_key(player, game, sound_manager, game_text, items):
    # Mock the game object
    player.current_room = game.locations["room_a"]
    assert player.current_room.name == game.locations["room_a"].name
    player.inventory.append(items["key_b"])
    assert player.inventory[0].name == game.locations[player.current_room.options.get('room_b')[0]].required_item

    player.move("room_b", game, game_text, sound_manager)
    assert player.current_room.name == game.locations["room_b"].name

def test_move_invalid_noun(player, game, sound_manager, capsys, game_text):
    player.current_room = game.locations["room_a"]
    result = player.move("invalid room", game, game_text, sound_manager)
    assert result == game_text['no_move']

def test_move_invalid_with_key(player, game, sound_manager, game_text, capsys):
    # Mock the game object
    player.current_room = game.locations["room_b"]
    assert game.locations[player.current_room.options.get('room_a')[0]].required_item
    captured = player.move("room_a", game, game_text, sound_manager)
    assert player.current_room.name != game.locations["room_a"].name
    assert captured == game_text['no_item'].format(no_item=game.locations["room_a"].required_item)


# Define test cases for picking up items
def test_take_item(player, game, sound_manager, game_text, items):
    # Mock the game object
    player.current_room = game.locations["room_a"]
    assert player.current_room.name == game.locations["room_a"].name

    # Try to pick up an item that exists in the room
    item_to_pick_up = items["key_a"]
    player.take_item(item_to_pick_up.name, "item_pickup_sound.wav", game_text, sound_manager)
    assert item_to_pick_up in player.inventory
    assert item_to_pick_up not in player.current_room.items

def test_take_item_invalid(player, game, sound_manager, game_text, capsys):
    # Mock the game object
    player.current_room = game.locations["room_b"]
    assert player.current_room.name == game.locations["room_b"].name

    # Try to pick up an item in an empty room
    captured = player.take_item("key_b", "item_pickup_sound.wav", game_text, sound_manager)

    assert captured == game_text["item_none"].format(item_name="key_b")

# Define test cases for using items
def test_use_item(player, game, sound_manager, game_text, items):
    # Mock the game object
    player.current_room = game.locations["room_a"]
    assert player.current_room.name == game.locations["room_a"].name

    # Add an item to the player's inventory
    item_to_use = items["key_a"]
    player.inventory.append(item_to_use)
    assert item_to_use in player.inventory
    # Try to use the item in the current room
    player.use_item(item_to_use.name, game_text)
    assert item_to_use not in player.inventory
    assert item_to_use in player.current_room.items

def test_use_item_invalid(player, game, sound_manager, game_text, capsys):
    # Mock the game object
    player.current_room = game.locations["room_a"]
    assert player.current_room.name == game.locations["room_a"].name
    # Try to use an item not in the player's inventory
    captured = player.use_item("key_a", game_text)
    
    assert captured == game_text["no_use"]

def test_inventory_list(player, capsys, game_text, items):
    # Mock the player's inventory
    player.inventory = [items["key_a"], items["key_b"]]
    # Call the inventory_list method
    captured = player.inventory_list(game_text)
    # Verify the output matches the expected format
    expected_output = game_text["inventory"]
    for item in player.inventory:
        expected_output += f"\n{item.name}"
    assert captured.strip() == expected_output.strip()

def test_inventory_empty(player, capsys, game_text, items):
    # Call the inventory_list method
    captured = player.inventory_list(game_text)
    expected_output = game_text["empty"]
    assert captured == expected_output


# Define a test case for the advance_time method
def test_advance_time(player, game_text):
    # Set the player's current room delay
    player.current_room = MagicMock()
    player.current_room.delay = 15
    # Call the advance_time method with a delay of 15 minutes
    player.advance_time(game_text, minutes=15)
    # Verify that the current time has been updated
    assert player.current_time == 465  # 450 + 15 = 465
    # Set the player's current room delay to 0
    player.current_room.delay = 0
    # Call the advance_time method with a delay of 10 minutes
    player.advance_time(game_text, minutes=10)
    # Verify that the current time has been updated
    assert player.current_time == 475  # 465 + 10 = 475


# Define a test case for the advance_time method
def test_advance_time_late(player, game_text):
    # Set the player's current room delay
    player.current_room = MagicMock()
    player.current_room.delay = 200
    printer = MagicMock()
    try:
        player.advance_time(game_text, player.current_room.delay, printer=printer)
    except SystemExit as e:
        assert e.code == 0


# Define a test case for the talk_npc method
def test_talk_npc(player, game, game_text, capsys):
    # Set up a mock location with NPC options
    player.current_room = MagicMock()
    player.current_room.options = {"npc": ["room_a"]}

    # Call the talk_npc method with a valid NPC name
    player.talk_npc("npc", game, game_text)

    # Verify that the current room has been updated to the destination room
    assert player.current_room.name == "room_a"

    # Call the talk_npc method with an invalid NPC name
    captured = player.talk_npc("invalid_npc", game, game_text)

    assert captured == game_text["no_npc"].format(noun="invalid_npc")

# Define a test case for the display_status method
def test_display_status(player, game_text, capsys):
    # Set the player's current time to 480 (8:00 AM)
    player.current_time = 480

    # Call the display_status method
    captured = player.display_status(game_text)

    # Verify that the output contains the current time in the expected format
    assert "CURRENT TIME: 08:00am" in captured

# Define a test case for the look_around method
def test_look_around(player, game, game_text, capsys):
    # Set up a mock location with description and items
    player.current_room = game.locations["room_a"]

    # Call the look_around method
    captured = player.look_around(game, game_text)

    # Verify that the output contains the room description and item names
    assert game.locations["room_a"].description in captured
    for item in game.locations["room_a"].items:
        assert item.name in captured

# Define a test case for the look_around method
def test_look_around_npc(player, game, game_text, capsys):
    # Set up a mock location with description and items
    assert game.locations["guard"].name
    player.current_room = game.locations["guard"]
    assert player.current_room.name
    # Call the look_around method
    captured = player.look_around(game, game_text)

    # Verify that the output contains the room description and item names
    assert game.locations["guard"].message in captured
    assert any(response in captured for response in game.locations["guard"].random_response)

# Define a test case for the save_game method
def test_save_game(player, game, saved_game_filename, items):
    player.name = "Test Player"
    player.inventory = [items["key_a"], items["key_b"]]
    player.current_room = game.locations["room_a"]
    player.current_room.name = game.locations["room_a"].name
    player.current_time = 500

    # Call the save_game method
    player.save_game(saved_game_filename)

    # Verify that the saved game file exists
    assert os.path.exists(saved_game_filename)

    # Load the saved game data from the file
    with open(saved_game_filename, 'r') as f:
        saved_data = json.load(f)

    # Verify the saved game data
    assert saved_data["name"] == player.name
    for item in saved_data["inventory"]:
        assert item in [inventory_item.name for inventory_item in player.inventory]
    assert saved_data["current_room"] == player.current_room.name
    assert saved_data["current_time"] == player.current_time

# Define a test case for the load_game method
def test_load_game(player, game, load_game_filename):
    # Create a saved game file with sample data
    with open(load_game_filename, 'r') as f:
        saved_data = json.load(f)

    # Call the load_game method to load the saved game
    loaded_player = player.load_game(game, load_game_filename)

    # Verify the loaded player's attributes
    assert loaded_player.name == saved_data.get("name")
    for item in loaded_player.inventory:
        assert item.name in saved_data.get("inventory")
    assert loaded_player.inventory[0].name == saved_data.get("inventory")[0]
    assert loaded_player.current_room.name == saved_data.get("current_room")
    assert loaded_player.current_time == saved_data.get("current_time")
