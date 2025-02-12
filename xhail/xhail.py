from abductor import Abductor, Example, Modeh
from parser import parseProgram
from structures import Modeb
from terms import Fact

# ---------- string -> Example() | Modeh() | string(background) ---------- #

def separate(result):
    examples = []
    modehs = []
    modebs = []
    for item in result:
        print(item)
        if isinstance(item, Example):
            examples.append(item)
        elif isinstance(item, Modeb):
            modebs.append(item)
        elif isinstance(item, Modeh):
            modehs.append(item)
    return examples, modehs, modebs

if __name__ == '__main__':
    # ---------- read and parse input program ---------- #
    file = open('test.lp', 'r', encoding="utf-8")
    data = file.read()

    #data = """
    #modeb not cars(mole(+cat, -badger), +cat).
    #modeh bright(-right).
    #example car(car(yes)).
    #"""

    result = parseProgram(data)
    print(result)
    E, H, B = separate(result)
    file.close()

    temp_background = '''
    bird(X) :- penguin(X).
    bird(a).
    bird(b).
    bird(c).
    penguin(d).
    '''

    # ---------- abduction ---------- #
    abductor = Abductor(E, H, temp_background)
    program = abductor.createProgram()
    results = abductor.callClingo(program)

    
