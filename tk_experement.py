import tkinter as tk

from app.label_printer import LabelPrinter

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")  # Set window size to 800x800

    help_label = tk.Label(root, text="", anchor="center", justify="center")
    help_label.grid(row=0, column=0, sticky="nsew")
    help_label.pack(expand=True, fill="both")
    
    help_printer = LabelPrinter(help_label)
    
    main_label = tk.Label(root, text="", anchor="center", justify="center")
    main_label.grid(row=0, column=0, sticky="nsew")
    main_label.pack(expand=True, fill="both")
    
    main_printer = LabelPrinter(main_label)

    # inital text
    help_printer.print("help text")
    help_printer.print("more help text")
    help_printer.update()
    # clear label
    help_printer.clear()
    help_printer.update()
    #add new text
    printer.print("new help text")
    printer.update()

    root.mainloop()
