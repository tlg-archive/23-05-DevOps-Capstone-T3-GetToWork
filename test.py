from GetToWork import Player, Item, Location
import pytest

def test_player_take_item(game_text):
    player = Player("Test Player")
    item_name = "Test Item"
    item = Item(item_name, "Test Description")
    player.current_room = Location("Test Room", "Test Description", [], 0, "test-key")
    player.current_room.add_item(item)
    game_text = game_text["grab_item"]
    player.take_item(item_name)
    assert item in player.inventory
    assert item not in player.current_room.items


if __name__ == '__main__':
    pytest.main()