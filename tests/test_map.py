import json
import os
from typing import Any, Protocol
from unittest.mock import MagicMock
import pytest
from pytest import CaptureFixture, MonkeyPatch
from app.map import Map


# Define a fixture to load the game_text JSON file
@pytest.fixture
def game_text():
    with open(os.path.realpath("json/game-text.json"), "r") as file:  # Replace with the actual path to your game_text.json
        return json.load(file)


# Define a fixture for the map_file variable
@pytest.fixture
def map_file():
    return os.path.realpath("tests/test_map.txt")  # Replace with the actual path to your map file

# Define a fixture to create an instance of the Map class for testing
@pytest.fixture
def sample_map(map_file: str):
    return Map(map_file)


class Location(Protocol):
    name: str
    map_key: str

class Player(Protocol):
    current_room: Location

# Define a custom protocol for the mock Game
class Game(Protocol):
    player: Player

# Define a fixture to create a mock Game object for testing
@pytest.fixture
def game_mock():
    game: Game = MagicMock(spec=Game)
    player: Player = MagicMock(spec=Player)
    current_room: Location = MagicMock(spec=MagicMock(spec=Location))
    current_room.name = "example_room"  # Adjust as needed
    current_room.map_key = "[1]"  # Adjust as needed
    player.current_room = current_room
    game.player = player
    return game

def test_update_map_0(sample_map: Map, game_mock: Game):
    # Mock the file read to avoid actual file operations
    sample_map.map_list = ["example_room[1] example_room[2]", "Bus Events[3] Car Events[4] Coffee Shop[5]"]
    tokens = []
    for line in sample_map.map_list:
        split_lines = line.split()
        for split in split_lines:
            tokens.append(split)
    sample_map.update_map(game_mock)
    assert any(game_mock.player.current_room.map_key in token for token in tokens)
    assert any((">>" in line and game_mock.player.current_room.map_key in line) for line in sample_map.map_list)

def test_update_map_1(sample_map: Map, game_mock: Game):
    # Mock the file read to avoid actual file operations
    sample_map.map_list = ["example_room[1] example_room[2]", "Bus Events[3]", "Car Events[4]", "Coffee Shop[5]"]
    game_mock.player.current_room.map_key = '[3]'
    game_mock.player.current_room.name = 'bus events'
    sample_map.update_map(game_mock)
    assert any((">>" in line and game_mock.player.current_room.map_key in line)  for line in sample_map.map_list)

def test_update_map_2(sample_map: Map, game_mock: Game):
    # Mock the file read to avoid actual file operations
    sample_map.map_list = ["example_room[1] example_room[2]", "Bus Events[3]", "Car Events[4]", "Coffee Shop[5]"]
    game_mock.player.current_room.map_key = '[4]'
    game_mock.player.current_room.name = 'car events'
    sample_map.update_map(game_mock)
    assert any((">>" in line and game_mock.player.current_room.map_key in line)  for line in sample_map.map_list)

def test_update_map_3(sample_map: Map, game_mock: Game):
    # Mock the file read to avoid actual file operations
    sample_map.map_list = ["example_room[1] example_room[2]", "Bus Events[3]", "Car Events[4]", "Coffee Shop[5]"]
    game_mock.player.current_room.map_key = '[5]'
    game_mock.player.current_room.name = 'coffee shop'
    sample_map.update_map(game_mock)
    assert any((">>" in line and game_mock.player.current_room.map_key in line) for line in sample_map.map_list)

def test_init(sample_map: Map, map_file: str):
    assert sample_map.map_file_path == map_file
    assert sample_map.map_list == []

def test_gen_map(sample_map: Map, map_file: str):
    sample_map.gen_map()
    with open(map_file, "r") as file:
        map_data = file.read()
    for line in sample_map.map_list:
        assert line in map_data

def test_show_map(capsys: CaptureFixture[str], sample_map: Map, game_text: Any):
    sample_map.map_list = sample_map.gen_map()  # Set some test data
    sample_map.show_map(game_text)
    captured = capsys.readouterr()

    for line in game_text["map_text"].split("\n"):
        assert line.strip() in captured.out.strip()
