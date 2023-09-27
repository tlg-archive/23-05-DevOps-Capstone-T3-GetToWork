import io
import json
import os
import pytest
from app.game import Game
from app.item import Item
from app.location import Location

from unittest.mock import MagicMock, patch
from typing import Protocol
from app.map import Map
from app.npc import NPC
from app.player import Player
from tests.test_Printer import TestPrinter

# Define a Protocol for a mock SoundManager
class MockSoundManager:
    def __init__(self) -> None:
        self.sound_enabled: bool = False
        self.current_volume: float = 0.5
        self.sfx_enabled: bool = False
        self.current_sfx_volume: float = 0.5
        self.volume_increment: float = 0.1

    def sound(self, sfx: str, script_dir: str) -> None:
        pass

    def sfx_sound(self, sfx_file: str) -> None:
        pass

    def toggle_sound(self) -> None:
        self.sound_enabled = not self.sound_enabled

    def volume_up(self) -> None:
        self.current_volume += self.volume_increment
        return self.current_volume

    def volume_down(self) -> None:
        self.current_volume -= self.volume_increment
        return self.current_volume

    def sfx_volume_up(self) -> None:
        self.current_sfx_volume += self.volume_increment
        return self.current_sfx_volume

    def sfx_volume_down(self) -> None:
        self.current_sfx_volume -= self.volume_increment
        return self.current_sfx_volume

    def toggle_fx(self) -> None:
        self.sfx_enabled = not self.sfx_enabled

@pytest.fixture
def debug_printer():
    return TestPrinter(print)

@pytest.fixture
def scene_printer():
    return TestPrinter(print)

@pytest.fixture
def result_printer():
    return TestPrinter(print)

@pytest.fixture
def status_printer():
    return TestPrinter(print)

@pytest.fixture
def items():
    result_items = {}
    with open(os.path.realpath("./tests/test_items.json"), 'r') as f:
        items = json.load(f)
    for item in items.keys():
        result_items[item] = Item(items[item]['name'], items[item]['description'])
    return result_items

@pytest.fixture
def script_dir():
    return os.path.dirname(os.path.realpath(__file__))

@pytest.fixture
def game(script_dir: str, debug_printer: TestPrinter, scene_printer: TestPrinter, result_printer: TestPrinter, status_printer: TestPrinter):
    game = Game(script_dir)
    game.npc_file = os.path.join(script_dir, 'test_npcs.json')
    game.load_npc()
    game.map_file = os.path.join(script_dir, 'test_map.txt')
    game.item_file = os.path.join(script_dir, 'test_items.json')
    game.location_file = os.path.join(script_dir, 'test_locations_for_game_test.json')
    with open(os.path.join(script_dir, 'test_save.json')) as save_file:
        game.save_data = json.load(save_file)
    game.debug_printer = debug_printer
    game.scene_printer = scene_printer
    game.result_printer = result_printer
    game.status_printer = status_printer
    return game

# Define a fixture to load the game_text JSON file
@pytest.fixture
def game_text():
    with open(os.path.realpath("./json/game-text.json"), "r") as file:  # Replace with the actual path to your game_text.json
        return json.load(file)

@pytest.fixture
def mock_sound_manager():
    return MockSoundManager()

# Test cases for the Game class

def test_game_init(game: Game, script_dir: str):
    assert isinstance(game, Game)
    assert isinstance(game.locations, dict)
    assert isinstance(game.location_music, dict)
    assert isinstance(game.items, list)
    assert isinstance(game.npcs, dict)
    assert game.player is None
    assert game.game_map is None
    assert game.game_data is None
    assert game.is_new_game is True
    with open(os.path.join(script_dir, 'test_save.json')) as save_file:
        data = json.load(save_file)
    assert game.save_data == data
    assert game.sound_manager
    assert game.game_time == '00:00'

def test_load_item_data(game: Game):
    item_data = game.load_item_data("key_a")
    with open(game.item_file, 'r') as f:
        items = json.load(f)
    assert item_data == items['key_a']

def test_load_game_data(game: Game):
    game.load_game_data()
    assert len(game.locations) > 0
    assert len(game.location_music) > 0
    assert all(isinstance(location, Location) or isinstance(location, NPC) for location in game.locations.values())

def test_handle_inventory(game: Game, game_text: dict[str, str], items: dict[str, Item]):
    game.player = Player('Test Player')
    game.player.inventory = [items['key_a'], items['key_b']]
    game.handle_inventory(game_text)
    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert "Inventory" in captured
    for item in game.player.inventory:
        assert item.name in captured


def test_parse_command_handle_take(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_take')

    # Test valid commands
    game.parse_command("take key_b", game_text)
    game.handle_take.assert_called_with("key_b", game.item_sound_file, game_text)

def test_parse_command_handle_use(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_use')

    # Test valid 'use' command
    game.parse_command("use item_c", game_text)
    game.handle_use.assert_called_with("item_c", game_text)
    #def handle_use(self, noun, game_text: dict[str, str]):



def test_parse_command_handle_look(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_look')

    # Test valid 'look' command
    game.parse_command("look mirror", game_text)
    game.handle_look.assert_called_with("mirror", game_text)


def test_parse_command_handle_talk(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_talk')

    # Test valid 'talk' command
    game.parse_command("talk npc_a", game_text)
    game.handle_talk.assert_called_with("npc_a", game_text)


def test_parse_command_invalid(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    # Test invalid command
    game.parse_command("invalid command", game_text)

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert game_text['invalid'] in captured


def test_parse_command_missing_noun(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    # Test invalid command
    game.parse_command("missing_noun", game_text)

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert game_text['need_noun'] in captured

def test_parse_command_save(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'save_game')

    game.parse_command("save game", game_text)
    game.save_game.assert_called()

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert game_text['save_game'] in captured

def test_parse_command_load(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'load_game')

    # Test valid 'buy' command
    game.parse_command("load game", game_text)
    game.load_game.assert_called()

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert game_text['load_game'] in captured

def test_handle_take(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager: MagicMock, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'key_a'

    #mocker.patch.object(game.player,'take_item')
    # Test valid 'take' command
    game.handle_take(noun, game.item_sound_file, game_text)
    assert noun in [item.name for item in game.player.inventory]
    assert noun not in [item.name for item in game.locations['room_a'].items]

def test_handle_use(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager: MagicMock, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'key_a'

    #mocker.patch.object(game.player, 'use_item')
    # Test valid 'use' command
    game.handle_use(noun, game_text)
    assert noun not in [item.name for item in game.player.inventory]
    assert noun in [item.name for item in game.locations['room_a'].items]

def test_handle_look(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager: MagicMock, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'mirror'

    mocker.patch.object(game, 'display_description')
    # Test valid 'look' command
    game.handle_look(noun, game_text)
    game.display_description.assert_called_with(noun, game_text)


    game.handle_look(None, game_text)
    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert game_text['look'] in captured

def test_handle_talk(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager: MagicMock, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_c']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'guard'

    game.handle_talk(noun, game_text)
    assert game.player.current_room == game.locations['guard']
    assert game.locations[noun].message in game.result_printer.content

def test_increment_time(game: Game):
    # Initialize the game time to 00:00
    game.game_time = '00:00'

    # Test incrementing time by 10 minutes
    game.increment_time()
    assert game.game_time == '00:10'

    # Test incrementing time to the next hour
    game.game_time = '00:50'
    game.increment_time()
    assert game.game_time == '01:00'

    # Test incrementing time to the next day
    game.game_time = '23:50'
    game.increment_time()
    assert game.game_time == '00:00'

def test_start_game(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    game.start_game()
    assert game.player.name != 'Test Player'
    assert game.player.current_room.name == 'Home'



def test_quit_command(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    assert not game.quitting
    game.parse_input(game_text, 'quit')
    assert game.quitting
    # Check if 'quit' was printed as a prompt
    assert game_text['quit'] in game.result_printer.content
    try:
        game.parse_input(game_text, 'yes')
    except SystemExit as e:
        assert e.code == 0


def test_quit_command_cancel(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    assert not game.quitting
    game.parse_input(game_text, 'quit')
    assert game.quitting
    # Check if 'quit' was printed as a prompt
    assert game_text['quit'] in game.result_printer.content
    game.parse_input(game_text, 'no')
    assert not game.quitting


def test_no_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    game.parse_input(game_text, '')

    assert '' == game.debug_printer.content


def test_help_command(game: Game, game_text: dict[str, str], mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    game.parse_input(game_text, 'help')
    assert game_text['help'] in game.result_printer.content


def test_inventory_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    game.parse_input(game_text, 'inventory')

    assert game_text["empty"] in game.result_printer.content

def test_time_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True

    game.parse_input(game_text, 'time')

    assert 'CURRENT TIME:' in game.result_printer.content


def test_map_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True
    game.game_map = Map(game.map_file)

    game.parse_input(game_text, 'map') # This should trigger the map command

    assert game_text['map_text'] in game.result_printer.content
    

def test_sound_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = MockSoundManager()
    game.is_new_game = True
    game.sound_manager.sound_enabled = True

    game.parse_input(game_text, 'toggle sound') # This should trigger the sound command

    assert not game.sound_manager.sound_enabled
    assert 'off' in game.result_printer.content

    game.parse_input(game_text, 'toggle sound') # This should trigger the sound command

    assert game.sound_manager.sound_enabled
    assert 'on' in game.result_printer.content

def test_volume_up_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager: MockSoundManager = mock_sound_manager
    game.is_new_game = True

    assert game.sound_manager.current_volume == 0.5
    game.parse_input(game_text, 'volume up')

    assert game.sound_manager.current_volume == 0.6
    assert game_text['vol_up'].format(current_volume=round(game.sound_manager.current_volume*100)) in game.result_printer.content
    

def test_volume_down_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager: MockSoundManager = mock_sound_manager
    game.is_new_game = True

    assert game.sound_manager.current_volume == 0.5
    game.parse_input(game_text, 'volume down')

    assert game.sound_manager.current_volume == 0.4
    assert game_text['vol_down'].format(current_volume=round(game.sound_manager.current_volume*100)) in game.result_printer.content


def test_sfx_down_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager: MockSoundManager = mock_sound_manager
    game.is_new_game = True

    assert game.sound_manager.current_sfx_volume == 0.5
    game.parse_input(game_text, 'sfx volume down')
    assert game.sound_manager.current_sfx_volume == 0.4
    assert game_text['sfx_down'].format(current_volume=round(game.sound_manager.current_sfx_volume*100)) in game.result_printer.content
    
def test_sfx_up_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager: MockSoundManager = mock_sound_manager
    game.is_new_game = True

    assert game.sound_manager.current_sfx_volume == 0.5
    game.parse_input(game_text, 'sfx volume up')
    assert game.sound_manager.current_sfx_volume == 0.6
    assert game_text['sfx_up'].format(current_volume=round(game.sound_manager.current_sfx_volume*100)) in game.result_printer.content
     

def test_toggle_sfx_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager: MockSoundManager = mock_sound_manager
    game.is_new_game = True
    assert game.sound_manager.sfx_enabled == False
    game.parse_input(game_text, 'toggle sfx')
    assert game.sound_manager.sfx_enabled == True
    assert 'sfx on' in game.result_printer.content
    game.parse_input(game_text, 'toggle sfx')
    assert game.sound_manager.sfx_enabled == False
    assert 'sfx off' in game.result_printer.content


def test_parse_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager: MockSoundManager = mock_sound_manager
    game.is_new_game = True
    mocker.patch.object(game, 'parse_command')

    game.parse_input(game_text, 'move north') # This should trigger the parse_command
    assert 'move north' in game.debug_printer.content
    game.parse_command.assert_called_with('move north'.strip().lower(), game_text)


def test_start_game_load_game(game: Game, game_text: dict[str, str], mocker, mock_sound_manager: MagicMock):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = False

    game.start_game()
    assert game.player.name != 'Test Player'
    assert game.player.current_room.name == 'room_a'

def test_save_game(game: Game, mocker, script_dir: str):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.player.current_time = 0
    game.save_game(os.path.join(script_dir, 'test_saving_game.json'))

    with open(os.path.join(script_dir, 'test_saving_game.json'), 'r') as f:
        data = json.load(f)
    
    assert data['name'] == game.player.name
    assert data['current_room'] == game.player.current_room.name
    for item in data['inventory']:
        assert item in game.player.inventory
    assert data['current_time'] == game.player.current_time
    os.remove(os.path.join(script_dir, 'test_saving_game.json'))

def test_load_game(game: Game, mocker, script_dir: str):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.player.current_time = 0
    game.load_game(os.path.join(script_dir, 'test_save.json'))

    with open(os.path.join(script_dir, 'test_save.json'), 'r') as f:
        data = json.load(f)
    
    assert data == game.save_data


def test_display_item_description(game: Game, game_text: dict[str, str], items: dict[str, Item]):
    game.load_game_data()

    # Test displaying the description of a mock item
    object_to_look = 'key_a'
    expected_output = items['key_a'].description
    game.display_description(object_to_look, game_text)

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert expected_output in captured

def test_display_location_description(game: Game, game_text: dict[str, str], items: dict[str, Item]):
    game.load_game_data()

    # Test displaying the description of a mock item
    object_to_look = 'room_a'
    expected_output = game.locations['room_a'].description
    game.display_description(object_to_look, game_text)

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert expected_output in captured


def test_display_invalid_description(game: Game, game_text: dict[str, str], items: dict[str, Item]):
    game.load_game_data()

    # Test displaying the description of a mock item
    object_to_look = 'invalid_object'
    expected_output = game_text["no_find_item"].format(object_to_look=object_to_look) 
    game.display_description(object_to_look, game_text)

    captured = '\n'.join([game.result_printer.content, game.debug_printer.content, game.scene_printer.content])
    assert expected_output in captured
