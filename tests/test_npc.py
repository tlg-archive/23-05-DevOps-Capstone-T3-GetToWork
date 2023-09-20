import pytest
from app.npc import NPC

@pytest.fixture
def sample_npc():
    return NPC(
        name="Sample NPC",
        message="Hello, traveler!",
        req_item=[],
        map_key="npc_key"
    )

def test_add_option(sample_npc):
    sample_npc.add_option("Action 1", "Location 1")
    assert "Action 1" in sample_npc.options
    assert sample_npc.options["Action 1"] == "Location 1"

def test_info(sample_npc):
    info_str = sample_npc.info()
    assert "name: Sample NPC" in info_str
    assert "message: Hello, traveler!" in info_str

def test_add_req_item(sample_npc):
    sample_npc.add_req_item("Required Item 1")
    assert "Required Item 1" in sample_npc.required_item

