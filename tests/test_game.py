import io
import json
import os
import pytest
from app.game import Game
from app.item import Item
from app.location import Location
from unittest.mock import MagicMock, patch
from typing import Protocol

from app.npc import NPC
from app.player import Player

# Define a Protocol for a mock SoundManager
class MockSoundManager(Protocol):
    def sound(self, sfx: str) -> None:
        pass

    def sfx_sound(self, sfx_file: str) -> None:
        pass

@pytest.fixture
def items():
    result_items = {}
    with open(os.path.realpath("./tests/test_items.json"), 'r') as f:
        items = json.load(f)
    for item in items.keys():
        result_items[item] = Item(items[item]['name'], items[item]['description'])
    return result_items

@pytest.fixture
def game():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    game = Game(script_dir)
    game.npc_file = os.path.join(script_dir, 'test_npcs.json')
    game.load_npc()
    game.item_file = os.path.join(script_dir, 'test_items.json')
    game.location_file = os.path.join(script_dir, 'test_locations_for_game_test.json')
    return game

# Define a fixture to load the game_text JSON file
@pytest.fixture
def game_text():
    with open(os.path.realpath("./json/game-text.json"), "r") as file:  # Replace with the actual path to your game_text.json
        return json.load(file)

@pytest.fixture
def mock_sound_manager():
    return MagicMock(spec=MockSoundManager)

# Test cases for the Game class

def test_game_init(game: Game):
    assert isinstance(game, Game)
    assert isinstance(game.locations, dict)
    assert isinstance(game.location_music, dict)
    assert isinstance(game.items, list)
    assert isinstance(game.npcs, dict)
    assert game.player is None
    assert game.game_map is None
    assert game.game_data is None
    assert game.is_new_game is True
    assert game.save_data is None
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

def test_handle_inventory(game: Game, game_text: dict[str, str], items: dict[str, Item], capsys):
    game.player = Player('Test Player')
    game.player.inventory = [items['key_a'], items['key_b']]
    game.handle_inventory(game_text)
    captured = capsys.readouterr()
    assert "Inventory" in captured.out.strip()
    for item in game.player.inventory:
        assert item.name in captured.out.strip()


def test_parse_command_handle_take(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_take')

    # Test valid commands
    game.parse_command("take key_b", game_text)
    game.handle_take.assert_called_with("key_b", game.item_sound_file, game_text)

def test_parse_command_handle_use(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
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


def test_parse_command_handle_drive(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_drive')

    # Test valid 'drive' command
    game.parse_command("drive car", game_text)
    game.handle_drive.assert_called_with("car", game_text, game.item_sound_file)


def test_parse_command_handle_board(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_board')

    # Test valid 'board' command
    game.parse_command("board bus", game_text)
    game.handle_board.assert_called_with("bus", game_text, game.item_sound_file)


def test_parse_command_handle_pull(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_pull')

    # Test valid 'pull' command
    game.parse_command("pull lever", game_text)
    game.handle_pull.assert_called_with("lever", game_text , game.item_sound_file) 


def test_parse_command_handle_look(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_look')

    # Test valid 'look' command
    game.parse_command("look mirror", game_text)
    game.handle_look.assert_called_with("mirror", game_text)


def test_parse_command_handle_talk(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_talk')

    # Test valid 'talk' command
    game.parse_command("talk npc_a", game_text)
    game.handle_talk.assert_called_with("npc_a", game_text)


def test_parse_command_handle_buy(game: Game, game_text: dict[str, str], mock_sound_manager, mocker):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'handle_buy')

    # Test valid 'buy' command
    game.parse_command("buy item_d", game_text)
    game.handle_buy.assert_called_with("item_d", game_text, game.item_sound_file)


def test_parse_command_invalid(game: Game, game_text: dict[str, str], mock_sound_manager, capsys):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    # Test invalid command
    game.parse_command("invalid command", game_text)

    captured = capsys.readouterr()
    assert game_text['invalid'] in captured.out


def test_parse_command_missing_noun(game: Game, game_text: dict[str, str], mock_sound_manager, capsys):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    # Test invalid command
    game.parse_command("missing_noun", game_text)

    captured = capsys.readouterr()
    assert game_text['need_noun'] in captured.out


def test_parse_command_save(game: Game, game_text: dict[str, str], mock_sound_manager, mocker, capsys):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'save_game')

    game.parse_command("save game", game_text)
    game.save_game.assert_called()

    captured = capsys.readouterr()
    assert game_text['save_game'] in captured.out


def test_parse_command_load(game: Game, game_text: dict[str, str], mock_sound_manager, mocker, capsys):
    # Mock the player and sound_manager objects
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.sound_manager = mock_sound_manager

    mocker.patch.object(game, 'load_game')

    # Test valid 'buy' command
    game.parse_command("load game", game_text)
    game.load_game.assert_called()

    captured = capsys.readouterr()
    assert game_text['load_game'] in captured.out

def test_handle_take(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'key_a'

    mocker.patch.object(game.player,'take_item')
    # Test valid 'take' command
    game.handle_take(noun, game.item_sound_file, game_text)
    game.player.take_item.assert_called_with(noun, game.item_sound_file, game_text, game.sound_manager)

def test_handle_use(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'item_a'

    mocker.patch.object(game.player, 'use_item')
    # Test valid 'use' command
    game.handle_use(noun, game_text)
    game.player.use_item.assert_called_with(noun, game_text)


def test_handle_drive(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'car'

    mocker.patch.object(game.player, 'move')
    # Test valid 'drive' command
    game.handle_drive(noun, game_text)
    game.player.move.assert_called_with(noun.title(), game, game_text, game.sound_manager)


def test_handle_board(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'bus'

    mocker.patch.object(game.player, 'move')
    # Test valid 'board' command
    game.handle_board(noun, game_text)
    game.player.move.assert_called_with(noun.title(), game, game_text, game.sound_manager)


def test_handle_pull(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'lever'

    mocker.patch.object(game.player, 'move')
    # Test valid 'pull' command
    game.handle_pull(noun, game_text)
    game.player.move.assert_called_with(noun.title(), game, game_text, game.sound_manager)


def test_handle_look(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
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
    captured = capsys.readouterr()
    assert game_text['look'] in captured.out


def test_handle_talk(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'npc_a'

    mocker.patch.object(game.player, 'talk_npc')
    # Test valid 'talk' command
    game.handle_talk(noun, game_text)
    game.player.talk_npc.assert_called_with(noun, game, game_text)


def test_handle_buy(game: Game, game_text: dict[str, str], items: dict[str, Item], mock_sound_manager, capsys, mocker):
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.current_room = game.locations['room_a']
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    noun = 'item_d'

    mocker.patch.object(game.player, 'move')
    # Test valid 'buy' command
    game.handle_buy(noun, game_text)
    game.player.move.assert_called_with(noun.title(), game, game_text, game.sound_manager)

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

def test_start_game_new_game_quit_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True
    mocker.patch.object(game.player, 'look_around')
    mocker.patch('builtins.input', side_effect=['quit', 'yes'])

    # Redirect stdout for capturing printed output
    mock_window_size = MagicMock()
    mock_window_size.columns = 80
    mock_window_size.rows = 24

    with patch('os.get_terminal_size', return_value=mock_window_size):  # Change the values as needed
        # Redirect stdout for capturing printed output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            game.start_game(game_text, debug=True, iterations_limit=2)

    # Check if 'quit' was printed as a prompt
    assert 'quit' in mock_stdout.getvalue()
    assert game_text['quit'] in mock_stdout.getvalue()



def test_start_game_new_game_quit_command_2(game: Game, game_text: dict[str, str], mocker, mock_sound_manager):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True
    mocker.patch.object(game.player, 'look_around')
    mocker.patch('builtins.input', side_effect=['quit', 'yes'])

    # Redirect stdout for capturing printed output
    mock_window_size = MagicMock()
    mock_window_size.columns = 80
    mock_window_size.rows = 24

    with patch('os.get_terminal_size', return_value=mock_window_size):  # Change the values as needed
        # Redirect stdout for capturing printed output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            game.start_game(game_text, debug=True, iterations_limit=1)

    # Check if 'quit' was printed as a prompt
    assert 'quit' in mock_stdout.getvalue()
    assert 


def test_start_game_new_game_no_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True
    mocker.patch('builtins.input', side_effect=[''])

    # Redirect stdout for capturing printed output
    mock_window_size = MagicMock()
    mock_window_size.columns = 10
    mock_window_size.rows = 24

    with patch('os.get_terminal_size', return_value=mock_window_size):  # Change the values as needed
        # Redirect stdout for capturing printed output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            game.start_game(game_text, debug=True, iterations_limit=1)

    assert '-----CURRENT LOCATION: Home-----' in mock_stdout.getvalue().strip()
    assert 'quit' not in mock_stdout.getvalue().strip()


def test_start_game_new_game_help_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True
    mocker.patch('builtins.input', side_effect=['help'])

    # Redirect stdout for capturing printed output
    mock_window_size = MagicMock()
    mock_window_size.columns = 80
    mock_window_size.rows = 24

    with patch('os.get_terminal_size', return_value=mock_window_size):  # Change the values as needed
        # Redirect stdout for capturing printed output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            game.start_game(game_text, debug=True, iterations_limit=1)

    # Check if 'quit' was printed as a prompt
    assert game_text['help'] in mock_stdout.getvalue().strip()


def test_start_game_new_game_inventory_command(game: Game, game_text: dict[str, str], mocker, mock_sound_manager):
    # Mock the player, sound_manager, and user input
    game.player = Player('Test Player')
    game.load_game_data()
    game.player.inventory = []
    game.sound_manager = mock_sound_manager
    game.is_new_game = True
    mocker.patch.object(game.player, 'look_around')
    mocker.patch.object(game, 'clear_screen')
    mocker.patch.object(game, 'create_window')
    mocker.patch('builtins.input', side_effect=['inventory'])

    # Redirect stdout for capturing printed output
    mock_window_size = MagicMock()
    mock_window_size.columns = 80
    mock_window_size.rows = 24

    with patch('os.get_terminal_size', return_value=mock_window_size):  # Change the values as needed
        # Redirect stdout for capturing printed output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            game.start_game(game_text, debug=True, iterations_limit=1)

    assert 'Your inventory is' in mock_stdout.getvalue().strip()