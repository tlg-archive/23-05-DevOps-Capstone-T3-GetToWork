import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("PanedWindow with Grid")

# Create a PanedWindow widget
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Create two frames to add to the PanedWindow
frame1 = tk.Frame(paned_window, background="red")
frame2 = tk.Frame(paned_window, background="blue")

# Add the frames to the PanedWindow
paned_window.add(frame1)
paned_window.add(frame2)

# Create widgets inside frame1 using grid layout
label1 = tk.Label(frame1, text="Hello, World!", padx=10, pady=10)
label1.grid(row=0, column=0)

button1 = tk.Button(frame1, text="Click Me")
button1.grid(row=1, column=0)

# Create widgets inside frame2 using grid layout
label2 = tk.Label(frame2, text="Hello, World!", padx=10, pady=10)
label2.grid(row=0, column=0)

button2 = tk.Button(frame2, text="Exit", command=root.quit)
button2.grid(row=1, column=0)

# Start the Tkinter main loop
root.mainloop()
