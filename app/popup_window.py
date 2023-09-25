from tkinter import *


class PopupWindow:
    def __init__(self, parent):
        self.parent = parent
        self.popup_open = False  # Flag to track if the popup is open

    def create_popup_window(self, game):
        if not self.popup_open:
            self.popup = Toplevel(self.parent)
            self.popup.title("Options")

            self.volume_label = Label(self.popup, text="Volume: 50%")
            self.volume_label.pack()
            self.volume_scale = Scale(self.popup, from_=0, to=10, orient=HORIZONTAL, command=lambda value: self.update_volume(value, game), showvalue=False)
            self.volume_scale.set(5)  # Set the initial volume to 50%
            self.volume_scale.pack() 

            self.sfx_volume_label = Label(self.popup, text="SFX Volume: 50%")
            self.sfx_volume_label.pack()
            self.sfx_volume_scale = Scale(self.popup, from_=0, to=10, orient=HORIZONTAL, command=lambda value: self.update_sfx_volume(value, game), showvalue=False)
            self.sfx_volume_scale.set(5)  # Set the initial volume to 50%
            self.sfx_volume_scale.pack()
            self.popup_open = True
            
            self.mute_checkbutton = Checkbutton(self.popup, text="Mute", command= lambda: self.toggle_mute(game))
            self.mute_checkbutton.pack()
    
            # Bind the destroy event to a callback function
            self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)
       
    def toggle_mute(self, game):
        game.sound_manager.toggle_sound()
        game.sound_manager.toggle_fx()

    def update_volume(self, value, game):
        self.volume_label.config(text=f"Volume: {(int(value)*10)}%")
        game.sound_manager.set_volume(int(value))

    def update_sfx_volume(self, value, game):
        self.sfx_volume_label.config(text=f"SFX Volume: {(int(value)*10)}%")
        game.sound_manager.set_sfx_volume(int(value))

    def close_popup(self):
        if hasattr(self, 'popup'):
            self.popup.destroy()
            self.popup_open = False
