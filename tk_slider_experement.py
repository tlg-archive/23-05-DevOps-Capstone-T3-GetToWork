import tkinter as tk
from tkinter import ttk

class VolumeControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Volume Control with Mute")
        self.muted = False

        # Create a Scale widget for volume control
        self.volume_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, label="Volume", command=self.update_volume)
        self.volume_scale.set(5)  # Set the initial volume to 5 (50%)
        self.volume_scale.pack()

        # Create a label to display the current volume
        self.volume_label = tk.Label(root, text="Volume: 50%")
        self.volume_label.pack()

        # Create a mute/unmute toggle button
        self.mute_button = ttk.Scale(
            root,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            length=60,
            command=self.toggle_mute,
            style="TScale",
        )
        self.mute_button.pack()

        # Create a label to show the mute state on the slider
        self.mute_state_label = tk.Label(root, text="Unmuted", fg="green")
        self.mute_state_label.pack()

        # Customize the ttk style to make the button look like a switch
        self.style = ttk.Style()
        self.style.configure("TScale", sliderthickness=15, sliderlength=40, troughcolor="gray")

    def update_volume(self, value):
        percentage = int(value) * 10  # Map the value from 0-10 to 0-100%
        self.volume_label.config(text=f"Volume: {percentage}%")

    def toggle_mute(self, value):
        self.muted = not bool(int(float(value)))
        if self.muted:
            self.volume_scale.config(state=tk.DISABLED)
            self.mute_state_label.config(text="Muted", fg="red")
            self.mute_button.set(0)  # Snap to the "Muted" position
        else:
            self.volume_scale.config(state=tk.NORMAL)
            self.mute_state_label.config(text="Unmuted", fg="green")
            self.mute_button.set(1)  # Snap to the "Unmuted" position

if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeControlApp(root)
    root.mainloop()
