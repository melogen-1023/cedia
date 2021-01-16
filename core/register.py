class Register:
    def __init__(self):
        self.register = []  # Source array

    def add_source(self, source):
        self.register.append(source)

    def execute(self):
        for source in self.register:
            print(source)
