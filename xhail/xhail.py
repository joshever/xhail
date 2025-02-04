from abductor import Example, Modeh

# ---------- string -> Example() | Modeh() | string(background) ---------- #
class Parser:
    examples = []
    modes = []
    background = []

    def __init__(self, program):
        self.program = program.splitlines()
        self.process()
    
    def processAll(self):
        for line in self.program:
            if line.split(" ")[0] == Example.KEY_WORD:
                self.examples.append(line[0:])
            if line.split(" ")[0] == Modeh.KEY_WORD:
                self.examples.append(line[0:])
            else:
                self.background.append(line)

    def processExamples(self):
        
        pass

    def processModes(self):
        pass

    def processBackground(self):
        pass
