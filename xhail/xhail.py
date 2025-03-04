from abduction import Abduction
from deduction import Deduction
from model import Model
from parser import Parser
from induction import Induction

if __name__ == '__main__':
    # ---------- read input ---------- #
    DEPTH = 1

    # ---------- parse data ---------- #
    parser = Parser()
    parser.loadFile('test.lp')
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

    # ---------- induction phase (3) ---------- #
    print("Induction...")
    induction = Induction(model)
    induction.runPhase()
    print("Complete.")
    
