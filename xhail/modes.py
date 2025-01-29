from terms import Atom

class Mode:
    pass

class Modeh(Mode):
    def __init__(self, r: str, s: Atom):
        self.r = r
        self.s = s

class Modeb(Mode):
    def __init__(self, r: str, s: Atom):
        self.r = r
        self.s = s