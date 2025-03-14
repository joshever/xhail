from xhail.reasoning.abduction import Abduction
from xhail.reasoning.deduction import Deduction
from xhail.reasoning.induction import Induction
from xhail.reasoning.model import Model
from xhail.parser.parser import Parser

if __name__ == '__main__':
    # ---------- read input ---------- #
    DEPTH = 3
    INPUT_FILENAME = 'test.lp'#'tests/deduction.lp'

    # ---------- parse data ---------- #
    parser = Parser()
    parser.loadFile(INPUT_FILENAME)
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate()

    # create empty clingo Model
    model = Model(EX, MH, MB, BG, DEPTH)

    # ---------- abduction phase (1) ---------- #
    print("Abduction...")
    abduction = Abduction(model)
    abduction.runPhase()
    print("Complete.")

    # ---------- deduction phase (2) ---------- #
    print("Deduction...")
    deduction = Deduction(model)
    deduction.runPhase()
    print("Complete.")

    # # ---------- induction phase (3) ---------- #
    # print("Induction...")
    # induction = Induction(model)
    # induction.runPhase()
    # print("Complete.")