from tkinter import *

def load_json_data():
    # Load data from a JSON file (replace 'your_file.json' with the actual file path)
    with open('/Users/ssanchez/Capstone-T3-GetToWork/json/location.json', 'r') as file:
        data = json.load(file)
    description_label.config(text=data.get('description', ''))

def start_game():
    load_json_data() 

def quit_game():
    app.quit()  # Close the GUI and end the application

app = Tk()
app.title("Game Window")
app.geometry("1550x1550")
image = PhotoImage(file="/Users/ssanchez/Capstone-T3-GetToWork/json/title2.png")
#app.wm_iconphoto(True, icon_image)

app.configure(bg="black") 

#app.('500x500')
label = Label(app, image=image, bg="black")
label.pack()

description_label = Label(app, text="", wraplength=500, justify="left", bg="black", fg="white")
description_label.pack()

start_button = Button(app, text="Start", command=start_game)
quit_button = Button(app, text="Quit", command=quit_game)

start_button.pack()
quit_button.pack()

app.mainloop()