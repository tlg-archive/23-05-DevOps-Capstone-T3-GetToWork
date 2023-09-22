import tkinter as tk

from app.lable_printer import LabelPrinter

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")  # Set window size to 800x800

    label = tk.Label(root, text="", anchor="center", justify="center")
    label.grid(row=0, column=0, sticky="nsew")
    label.pack(expand=True, fill="both")
    
    printer = LabelPrinter(label)

    printer.print("Hello,", "world!")
    printer.print("This is a", "LabelPrinter.")
    printer.update()

    root.mainloop()
