from abductor import Abductor, Example, Modeh
from parser import parseProgram
from structures import Modeb
from terms import Clause, Fact

# ---------- string -> Example | Modeh | Modeb | Background ---------- #
def separate(result):
    examples = []
    modehs = []
    modebs = []
    background = []
    for item in result:
        if isinstance(item, Example):
            examples.append(item)
        elif isinstance(item, Modeb):
            modebs.append(item)
        elif isinstance(item, Modeh):
            modehs.append(item)
        elif isinstance(item, Clause):
            background.append(item)
    return examples, modehs, modebs, background

if __name__ == '__main__':
    # ---------- read input ---------- #
    file = open('test.lp', 'r', encoding="utf-8")
    data = file.read()

    # ---------- parse data ---------- #
    result = parseProgram(data)
    print(result)
    EX, MH, MB, BG = separate(result) #EX - examples, MH - modeh, MB - modeb, BG - background
    file.close()

    # ---------- abduction phase (1) ---------- #
    abductor = Abductor(EX, MH, BG)
    program = abductor.createProgram()
    results = abductor.callClingo(program)

    # ---------- deduction phase (2) ---------- #
    #TODO : deduce body components

    # ---------- induciton phase (3) ---------- #
    #TODO : induce kernel set (?)
