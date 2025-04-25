import argparse
from xhail.state.context import Context
from xhail.reasoning.abduction import Abduction
from xhail.reasoning.deduction import Deduction
from xhail.reasoning.induction import Induction
from xhail.parser.parser import Parser
import time

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

    if args.background == True:
        BG_string = open(args.bname, 'r', encoding="utf-8").read()
        BG.append(str(BG_string))

    # ---------- CONTEXT AND PHASES ---------- #
    context = Context(EX, MH, MB, BG, DEPTH, TIMEOUT)
    phases = [Abduction(context), Deduction(context), Induction(context)]

    # ---------- MAIN LOOP ---------- #
    start = time.time()
    while context.getState() == 'solving':
        for phase in phases:
            phase.run()
            current = time.time() - start
            if current > TIMEOUT:
                context.setState('TIMEOUT')
        print([str(d) for d in context.getDelta()])
    
    # ---------- DISPLAY RESULTS ---------- #
    print(context.getState())
    if context.state == 'COMPLETE':
        print("deltas:", [str(d) for d in context.getDelta()])
        print("kernel:", [str(k) for k in context.getKernel()])
        print("hypothesis:", [str(h) for h in context.getHypothesis()])

# ---------- START AND COLLATE INPUT ---------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyXHAIL input parameters.")
    parser.add_argument('--depth', type=int, default=2, help='Depth of hypothesis clauses')
    parser.add_argument('--verbose', type=bool, default=True, help='Save Clingo programs')
    parser.add_argument('--fname', type=str, default='tests/test.lp', help='Input program filename')
    parser.add_argument('--timeout', type=int, default=10, help='Clingo Solver Timeout')
    parser.add_argument('--background', type=bool, default=False, help='Add additional Background program')
    parser.add_argument('--bname', type=str, default='', help='Background program filename')
    args = parser.parse_args()
    main(args)