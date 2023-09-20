class NPC:
    def __init__(self, name, message, req_item, map_key):
        self.name = name
        self.message = message
        self.random_response = []
        self.options = {}
        self.required_item = req_item
        self.map_key = map_key

    def add_option(self, action, loc):
        self.options[action] = loc

    def info(self):
        return f"name: {self.name}\nmessage: {self.message}\nresponse:{self.random_response}\noptions:{self.options}"

    def add_req_item(self, item):
        self.required_item.append(item)
