from typing import Protocol
import pytest
from unittest import mock
from app.sound_manager import SoundManager

# Mock the pygame.mixer.Sound class
class Sound(Protocol):
    filename: str

# Mock the pygame.mixer.Channel class
class Channel(Protocol):
    played_sound: Sound
    volume: float
    paused: bool

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def play(self, sound, loops: int = 0):
        pass

    def set_volume(self, volume: float):
        self.volume = round(volume, 1)

# Create a fixture for the SoundManager instance
@pytest.fixture
def sound_manager():
    sound_manager = SoundManager()
    sound_manager.music_channel: Channel = mock.MagicMock(spec=Channel)
    sound_manager.music_channel.played_sound: Sound = mock.MagicMock(spec=Sound)
    sound_manager.music_channel.played_sound.filename: str = 'test_music.wav'
    sound_manager.music_channel.volume: float = float(sound_manager.current_volume)
    sound_manager.sfx_channel: Channel = mock.MagicMock(spec=Channel)
    sound_manager.sfx_channel.played_sound: Sound = mock.MagicMock(spec=Sound)
    sound_manager.sfx_channel.played_sound.filename: str = 'test_sfx.wav'
    sound_manager.sfx_channel.volume: float = float(sound_manager.current_sfx_volume)
    return sound_manager

def test_sound(sound_manager):
    with mock.patch('pygame.mixer.Sound', return_value=mock.MagicMock(filename='test_music.wav', spec=Sound)):
        sound_manager.sound('test_music.wav')
        assert sound_manager.music_channel.played_sound.filename == 'test_music.wav'
        assert sound_manager.music_channel.volume == sound_manager.current_volume

def test_sfx_sound(sound_manager):
    with mock.patch('pygame.mixer.Sound', return_value=mock.MagicMock(filename='test_sfx.wav', spec=Sound)):
        sound_manager.sfx_sound('test_sfx.wav')
        assert sound_manager.sfx_channel.played_sound.filename == 'test_sfx.wav'
        assert sound_manager.sfx_channel.volume == sound_manager.current_sfx_volume

# Add more test cases for other SoundManager methods...

def test_toggle_sound(sound_manager):
    sound_manager.sound_enabled = True
    sound_manager.toggle_sound()
    assert sound_manager.sound_enabled is False
    sound_manager.toggle_sound()
    assert sound_manager.sound_enabled is True

def test_toggle_fx(sound_manager):
    sound_manager.sfx_enabled = True
    sound_manager.toggle_fx()
    assert sound_manager.sfx_enabled is False
    sound_manager.toggle_fx()
    assert sound_manager.sfx_enabled is True

# Add test cases for raising and lowering music volume
def test_volume_up(sound_manager):
    initial_volume = sound_manager.current_volume
    sound_manager.volume_up()
    assert sound_manager.current_volume == initial_volume + sound_manager.volume_increment

def test_volume_up_max(sound_manager):
    for _ in range(0, 10):
        sound_manager.volume_up()
    assert sound_manager.current_volume == 10

def test_volume_down(sound_manager):
    initial_volume = sound_manager.current_volume
    sound_manager.volume_down()
    assert sound_manager.current_volume == initial_volume - sound_manager.volume_increment

def test_volume_down_min(sound_manager):
    for _ in range(0, 10):
        sound_manager.volume_down()
    assert sound_manager.current_volume == 0

def test_sfx_volume_up(sound_manager):
    initial_sfx_volume = sound_manager.current_sfx_volume
    sound_manager.sfx_volume_up()
    assert sound_manager.current_sfx_volume == initial_sfx_volume + sound_manager.volume_increment

def test_sfx_volume_up_max(sound_manager):
    for _ in range(0, 10):
        sound_manager.sfx_volume_up()
    assert sound_manager.current_sfx_volume == 10

def test_sfx_volume_down(sound_manager):
    initial_sfx_volume = sound_manager.current_sfx_volume
    sound_manager.sfx_volume_down()
    assert sound_manager.current_sfx_volume == initial_sfx_volume - sound_manager.volume_increment

def test_sfx_volume_down_min(sound_manager):
    for _ in range(0, 10):
        sound_manager.sfx_volume_down()
    assert sound_manager.current_sfx_volume == 0
