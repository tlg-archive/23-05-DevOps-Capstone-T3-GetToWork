import tkinter as tk

def hide_label(event):
    label.pack_forget()

# Create the main window
root = tk.Tk()
root.title("Hide Label on Enter")

# Create a label to be hidden
label = tk.Label(root, text="Label to be hidden")
label.pack(pady=20)

# Bind the Enter key press event to the hide_label function
root.bind('<Return>', hide_label)

# Start the main loop
root.mainloop()
