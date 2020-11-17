import random

class Citizen:
    def __init__(self, coconuts):
        self.coconuts = coconuts

    def add_coconut(self):
        self.coconuts += 1

    def dec_coconut(self):
        if self.coconuts > 0:
            self.coconuts -= 1
    
    def confront(self, other):
        win = random.choice([True, False])

        if win:
            self.add_coconut()
            other.dec_coconut()
        else:
            self.dec_coconut()
            other.add_coconut()