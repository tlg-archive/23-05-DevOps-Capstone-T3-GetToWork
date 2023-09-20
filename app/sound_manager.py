#SOUND FUNCTIONALITY BELOW
import math
import os
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        self._volume_increment = 1
        self.current_volume = 4
        self.current_sfx_volume = 6
        self.sound_enabled = True
        self.sfx_enabled = True

    @property
    def volume_increment(self):
        return self._volume_increment

    def sound(self, sound_file, script_dirs):
        #print(sound_file.split('/'))
        song_name_list = sound_file.split('/')
        array_len = len(song_name_list)

        sound_file_path = os.path.join(script_dirs, 'sfx', song_name_list[array_len-1])
        
        background_music = pygame.mixer.Sound(sound_file_path) #sound_file formerly
        self.music_channel.play(background_music, loops=-1)  # -1 loops indefinitely
        self.music_channel.set_volume(self.current_volume)

    #PLAYS THE SOUND EFFECT SFX - USED IN Player.take_item()
    def sfx_sound(self, sound_file: str):
        if self.sfx_enabled:
            sfx_music = pygame.mixer.Sound(sound_file)
            self.sfx_channel.play(sfx_music)  # -1 loops indefinitely
            self.sfx_channel.set_volume(self.current_sfx_volume)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.music_channel.unpause()
        else:
            self.music_channel.pause() 

    def toggle_fx(self):
        self.sfx_enabled = not self.sfx_enabled
        if self.sfx_enabled:
            self.sfx_channel.unpause()
        else:
            self.sfx_channel.pause()       

    def volume_up(self):
        self.current_volume += self._volume_increment
        if self.current_volume > 10:
            self.current_volume = 10
        self.music_channel.set_volume(self.current_volume/10)

    def volume_down(self):
        self.current_volume -= self._volume_increment
        if self.current_volume < 0:
            self.current_volume = 0
        self.music_channel.set_volume(self.current_volume/10)

    def sfx_volume_up(self):
        self.current_sfx_volume += self._volume_increment
        if self.current_sfx_volume > 10:
            self.current_sfx_volume = 10
        self.sfx_channel.set_volume(self.current_volume/10)

    def sfx_volume_down(self):
        self.current_sfx_volume -= self._volume_increment
        if self.current_sfx_volume < 0:
            self.current_sfx_volume = 0
        self.sfx_channel.set_volume(self.current_volume/10)
