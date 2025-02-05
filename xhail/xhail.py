from abductor import Example, Modeh
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
        print(self.program)
        self.processAll()

    def generateAtom(self, stringAtom):
        print(stringAtom)
        pieces = re.split(r'[(),]', stringAtom)
        terms = []
        for piece in pieces[1:-1]:
            if piece[0] == '+' or piece[0] == '-':
                terms.append(PlaceMarker(piece[0], piece[1:]))
            else:
                terms.append(Normal(piece))
        atom = Atom(pieces[0], terms)
        return atom
    
    def processAll(self):
        for line in self.program:
            print(line.split(" ")[0])
            if line.split(" ")[0] == Example.KEY_WORD:
                self.examples.append(line[0:])
            elif line.split(" ")[0] == Modeh.KEY_WORD or line.split(" ")[0] == '#modeb': #update later
                self.modes.append(line[0:])
            elif line != '' and line[0] != '%':
                self.background.append(line)
            else:
                pass

    def parseExamples(self):
        result = []
        for example in self.examples:
            example = example.split(" ")[1:]
            if example[0] == 'not':
                negation = True
                atom = self.generateAtom(example[1])
            else:
                negation = False
                atom = self.generateAtom(example[0])
            parsedExample = Example(atom, negation)
            result.append(parsedExample)
        self.parsedExamples = result
        return result

    def parseModes(self):
        result = {'M+': [], 'M-': []}
        for mode in self.modes:
            mode = mode.split(" ")
            if mode[0] == Modeh.KEY_WORD:
                atom = self.generateAtom(mode[1])
                parsedMode = Modeh(atom, '*')
                print(parsedMode)
                result['M+'] = result['M+'] + [parsedMode]
            else:
                pass
        print(result['M+'])
        self.parseModes = result
        return result


    def processBackground(self):
        return self.background

if __name__ == '__main__':
    file = open('test.lp', 'r')
    parser = Parser(file.read())
    print("examples: ", [str(e) for e in parser.parseExamples()])
    print("modes: ", [str(m) for m in parser.parseModes()['M+']])
    print("background: ", parser.processBackground())
