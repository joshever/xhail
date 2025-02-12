from abductor import Abduction
from parser import parseProgram
from structures import Example, Modeh, Modeb
from terms import Clause

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
    parsedData = parseProgram(data)
    EX, MH, MB, BG = separate(parsedData) #EX - examples, MH - modeh, MB - modeb, BG - background
    file.close()

    # ---------- abduction phase (1) ---------- #
    abduction = Abduction(EX, MH, BG)
    abduction.createProgram()
    abduction.callClingo()
    delta = abduction.getDelta()

    # ---------- deduction phase (2) ---------- #
    

    # ---------- induction phase (3) ---------- #
    #TODO : induce kernel set (?)
