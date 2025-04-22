import argparse
from xhail.reasoning.abduction import Abduction
from xhail.reasoning.deduction import Deduction
from xhail.reasoning.induction import Induction
from xhail.reasoning.model import Model
from xhail.parser.parser import Parser

def main(args):
    # ---------- read input ---------- #
    DEPTH = args.depth
    INPUT_FILENAME = args.fname

    # ---------- parse data ---------- #
    parser = Parser()
    parser.loadFile(INPUT_FILENAME)
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate()    

    model = Model(EX, MH, MB, BG, DEPTH)
    # IF HYPOTHESIS == [] -> REPEAT UNTIL MODEH MIN == MODEH MAX OR ABDUCTION UNSATISFIED.
    
    abduction, deduction, induction = Abduction(model), Deduction(model), Induction(model)
    
    abduction.runPhase()
    deduction.runPhase()
    induction.runPhase()
    
    print("deltas:", [str(d) for d in model.getDelta()])
    print("kernel:", [str(k) for k in model.getKernel()])
    print("hypothesis:", [str(h) for h in model.getHypothesis()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyXHAIL input parameters.")
    parser.add_argument('--depth', type=int, default=3, help='Depth of hypothesis clauses')
    parser.add_argument('--verbose', type=bool, default=True, help='Save Clingo programs')
    parser.add_argument('--fname', type=str, default='tests/test.lp', help='Input program filename')
    args = parser.parse_args()
    main(args)