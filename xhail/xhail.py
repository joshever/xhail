from abductor import Abductor, Example, Modeh
import re
from terms import Atom, Normal, PlaceMarker

# ---------- string -> Example() | Modeh() | string(background) ---------- #
class Parser:
    examples = []
    modes = []
    background = []

    parsedExamples = []
    parsedModes = {'M+': [], 'M-': []}
    parsedBackground = []

    def __init__(self, program):
        self.program = program.splitlines()
        self.parseAll()

    def parseAtom(self, stringAtom):
        pieces = re.split(r'[(),]', stringAtom)
        terms = []
        for piece in pieces[1:-1]:
            if piece[0] == '+' or piece[0] == '-':
                terms.append(PlaceMarker(piece[0], piece[1:]))
            else:
                terms.append(Normal(piece))
        atom = Atom(pieces[0], terms)
        return atom
    
    def parseAll(self):
        for line in self.program:
            if line.split(" ")[0] == Example.KEY_WORD:
                self.examples.append(line[0:])
            elif line.split(" ")[0] == Modeh.KEY_WORD or line.split(" ")[0] == '#modeb': #update later
                self.modes.append(line[0:])
            elif line != '' and line[0] != '%':
                self.background.append(line)
            else:
                pass
        self.parseExamples()
        self.parseModes()
        self.parseBackground()

    def parseExamples(self):
        result = []
        for example in self.examples:
            example = example.split(" ")[1:]
            if example[0] == 'not':
                negation = True
                atom = self.parseAtom(example[1])
            else:
                negation = False
                atom = self.parseAtom(example[0])
            parsedExample = Example(atom, negation)
            result.append(parsedExample)
        self.parsedExamples = result
        return result

    def parseModes(self):
        result = {'M+': [], 'M-': []}
        for mode in self.modes:
            mode = mode.split(" ")
            if mode[0] == Modeh.KEY_WORD:
                atom = self.parseAtom(mode[1])
                parsedMode = Modeh(atom, '*')
                result['M+'] = result['M+'] + [parsedMode]
            else:
                pass
        self.parsedModes = result
        return result
    
    def parseBackground(self):
        self.parsedBackground = self.background
        return self.background

if __name__ == '__main__':
    file = open('test.lp', 'r', encoding="utf-8")
    parser = Parser(file.read())
    file.close()

    # ABDUCTION
    abductor = Abductor(parser.parsedExamples, parser.parsedModes['M+'], parser.parsedBackground)
    program = abductor.createProgram()
    results = abductor.callClingo(program)

    #DEDUCTION


    print(results[0])
    
