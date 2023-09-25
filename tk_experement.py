import tkinter as tk

class PopupWindow:
    def __init__(self, parent):
        self.parent = parent
        self.popup_open = False  # Flag to track if the popup is open

    def create_popup_window(self):
        if not self.popup_open:
            self.popup = tk.Toplevel(self.parent)
            self.popup.title("Options")

            # Create a Scale widget for volume control inside the popup window
            self.volume_scale = tk.Scale(self.popup, from_=0, to=10, orient=tk.HORIZONTAL, label="Volume", command=self.update_volume)
            self.volume_scale.set(5)  # Set the initial volume to 50%
            self.volume_scale.pack()

            # Create a label to display the current volume
            self.volume_label = tk.Label(self.popup, text="Volume: 50%")
            self.volume_label.pack()

            # Set the flag to indicate that the popup is open
            self.popup_open = True

            # Bind the destroy event to a callback function
            self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

    def update_volume(self, value):
        if hasattr(self, 'volume_label'):
            self.volume_label.config(text=f"Volume: {(int(value) * 10)}%")

    def close_popup(self):
        if hasattr(self, 'popup'):
            self.popup.destroy()
            self.popup_open = False

# Create the main window
window = tk.Tk()
window.title("Volume Slider Example")

# Create an instance of the PopupWindow class
popup_manager = PopupWindow(window)

# Create a button to open the popup window
options_button = tk.Button(window, text="Options", command=popup_manager.create_popup_window)
options_button.pack()

# Run the Tkinter event loop
window.mainloop()
