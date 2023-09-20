import pytest
from app.location import Location  # Replace 'your_module' with the actual module where the Location class is defined

# Define a fixture to create an instance of the Location class for testing
@pytest.fixture
def sample_location():
    return Location(
        name="Sample Location",
        description="A sample location",
        req_item=[],
        loc_delay=0,
        map_key="sample_key"
    )

# Test cases for the Location class methods
def test_add_option(sample_location):
    sample_location.add_option("Action 1", "Location 1")
    assert "Action 1" in sample_location.options
    assert sample_location.options["Action 1"] == "Location 1"

def test_add_item(sample_location):
    sample_location.add_item("Item 1")
    assert "Item 1" in sample_location.items

def test_add_req_item(sample_location):
    sample_location.add_req_item("Required Item 1")
    assert "Required Item 1" in sample_location.required_item

def test_info(sample_location):
    info_str = sample_location.info()
    assert "name: Sample Location" in info_str
    assert "description: A sample location" in info_str
