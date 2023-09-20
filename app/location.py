
class Location:
    def __init__(self, name, description, req_item, loc_delay,map_key):
        self.name = name
        self.description = description
        self.options = {}
        self.items = []
        self.required_item = req_item
        self.delay = loc_delay
        self.map_key = map_key

    def add_option(self, action, loc):
        self.options[action] = loc

    def add_item(self, item):
        self.items.append(item)

    def add_req_item(self, item):
        self.required_item.append(item)

    def info(self):
        return f"name: {self.name}\ndescription: {self.description}\items:{self.items}\noptions:{self.options}"
