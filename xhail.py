import argparse
from xhail.state.context import Context
from xhail.reasoning.abduction import Abduction
from xhail.reasoning.deduction import Deduction
from xhail.reasoning.induction import Induction
from xhail.parser.parser import Parser

def main(args):
    # ---------- COMMAND LINE ARGUMENTS ---------- #
    DEPTH = args.depth
    INPUT_FILENAME = args.fname
    TIMEOUT = args.timeout

    # ---------- PARSER ---------- #
    parser = Parser()
    parser.loadFile(INPUT_FILENAME)
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate()    

    # ---------- CONTEXT AND PHASES ---------- #
    context = Context(EX, MH, MB, BG, DEPTH, TIMEOUT)
    phases = [Abduction(context), Deduction(context), Induction(context)]

    # ---------- MAIN LOOP ---------- #
    while context.getState() == 'solving':
        for phase in phases:
            phase.run()
    
    # ---------- DISPLAY RESULTS ---------- #
    if context.state == 'complete':
        print("deltas:", [str(d) for d in context.getDelta()])
        print("kernel:", [str(k) for k in context.getKernel()])
        print("hypothesis:", [str(h) for h in context.getHypothesis()])
    else:
        print("UNSATISFIABLE")

# ---------- START AND COLLATE INPUT ---------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyXHAIL input parameters.")
    parser.add_argument('--depth', type=int, default=3, help='Depth of hypothesis clauses')
    parser.add_argument('--verbose', type=bool, default=True, help='Save Clingo programs')
    parser.add_argument('--fname', type=str, default='tests/test.lp', help='Input program filename')
    parser.add_argument('--timeout', type=int, default=10, help='Clingo Solver Timeout')
    args = parser.parse_args()
    main(args)