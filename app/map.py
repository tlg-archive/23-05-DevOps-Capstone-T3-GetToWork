class Map:
    def __init__(self, map_file: str):
        self.map_file_path = map_file
        self.map_list: list[str] = []

    def gen_map(self) -> list[str]:
        print(self.map_file_path)
        with open(self.map_file_path, "r") as file:
            map_list = file.readlines()
        return map_list

    def show_map(self, game_text: dict[str, str]):
        print(game_text["map_text"])
        for line in self.map_list:
            print(line)

    def update_map(self, game):
        current_key = game.player.current_room.map_key
        for index, line in enumerate(self.map_list):
            if current_key in line:
                try:
                    idx = line.index(game.player.current_room.name)
                except ValueError:
                    if "Bus Events" in line:
                        idx = line.index("Bus Events")
                    elif "Car Events" in line:
                        idx = line.index("Car Events")
                    else:
                        idx = line.index("Coffee Shop")
                updated_line = line[:idx] + ">> " + line[idx:]
                line = updated_line
                self.map_list[index] = updated_line

