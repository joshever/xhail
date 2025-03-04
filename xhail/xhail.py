from abduction import Abduction
from deduction import Deduction
from model import Model
from parser import Parser

if __name__ == '__main__':
    # ---------- read input ---------- #
    DEPTH = 2

    # ---------- parse data ---------- #
    parser = Parser()
    parser.loadFile('test.lp')
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate()

    # create empty clingo Model
    model = Model(EX, MH, MB, BG, DEPTH)

    # ---------- abduction phase (1) ---------- #
    abduction = Abduction(model)
    abduction.runPhase()

    # ---------- deduction phase (2) ---------- #
    deduction = Deduction(model)
    deduction.runPhase()

    # ---------- induction phase (3) ---------- #
    induction = Induction(model)
    induction.runPhase()
    
