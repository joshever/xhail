from terms import Atom

class Mode:
    def __init__(self, n, terms: Atom):
        self.n = n
        self.terms = terms

class ModeH(Mode):
    def __init__(self):
        super().__init__()

class ModeB(Mode):
    def __init__(self):
        super().__init__()