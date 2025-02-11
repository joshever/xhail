from abductor import Abductor, Example, Modeh
from parser import parseProgram
from structures import Modeb
from terms import Fact

# ---------- string -> Example() | Modeh() | string(background) ---------- #

if __name__ == '__main__':
    file = open('test.lp', 'r', encoding="utf-8")
    data = file.read()
    result = parseProgram(data)
    file.close()

    for clause in result:
        print(clause)

    # ABDUCTION
    #abductor = Abductor(parser.parsedExamples, parser.parsedModes['M+'], parser.parsedBackground)
    #program = abductor.createProgram()
    #results = abductor.callClingo(program)

    #DEDUCTION
    #print(results[0])
    
