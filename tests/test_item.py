import pytest
from app.item import Item


# Test the initialization of the Item class
def test_item_init():
    name = "Test Item"
    description = "This is a test item."
    item = Item(name, description)

    assert item.name == name
    assert item.description == description
    assert item.locations == []

# Test the __str__ method of the Item class
def test_item_str():
    name = "Test Item"
    description = "This is a test item."
    item = Item(name, description)

    assert str(item) == name

# Test adding locations to an Item
def test_add_location_to_item():
    item = Item("Test Item", "This is a test item.")
    location_name = "Test Location"

    item.locations.append(location_name)

    assert location_name in item.locations

# Test removing locations from an Item
def test_remove_location_from_item():
    item = Item("Test Item", "This is a test item.")
    location_name = "Test Location"

    item.locations.append(location_name)
    assert location_name in item.locations

    item.locations.pop(item.locations.index(location_name))
    assert location_name not in item.locations
