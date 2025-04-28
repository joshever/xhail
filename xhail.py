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

    isBackground = args.b
    BACKGROUND = args.bname

    isTimeout = args.t
    TIMEOUT = args.timeout

    isExpressive = args.e
    TIMELIMIT = args.timelimit
    MODELLIMIT = args.modellimit

    isVERBOSE = args.v
    
    # ---------- PARSER ---------- #
    parser = Parser()
    parser.loadFile(INPUT_FILENAME)
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate() 

    if isBackground:
        BG_string = open(BACKGROUND, 'r', encoding="utf-8").read()
        BG.append(str(BG_string))

    # ---------- CONTEXT AND PHASES ---------- #
    context = Context(EX, MH, MB, BG, DEPTH)
    context.setExpressivity(isExpressive, TIMELIMIT, MODELLIMIT)
    context.setVerbose(isVERBOSE)
    abduction, deduction, induction = Abduction(context), Deduction(context), Induction(context)
    phases = [abduction, deduction, induction]

    # ---------- MAIN LOOP ---------- #
    start = time.time()
    while context.getState() == 'solving':
        for phase in phases:
            phase.run()
            current = time.time() - start
            if isTimeout and current > TIMEOUT:
                context.setState('TIMEOUT')
        if context.hypothesis != []:
            context.setState('COMPLETE')
            continue
        inc = context.incrementModel()
        if not inc:
            incMin = abduction.incrementMin()
            if not incMin:
                context.setState('UNSATISFIABLE')
            else:
                pass
        else:
            pass
    
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
    parser.add_argument('--fname', type=str, default='tests/test.lp', help='Input program filename')
    parser.add_argument('-v', action='store_true')

    parser.add_argument('-e', action='store_true')
    parser.add_argument('--timelimit', type=int, default=10, help='Clingo Solver Timeout')
    parser.add_argument('--modellimit', type=int, default=10, help='Clingo Solver Model Limit')

    parser.add_argument('-b', action='store_true')
    parser.add_argument('--bname', type=str, default='', help='Background program filename')

    parser.add_argument('-t', action='store_true')
    parser.add_argument('--timeout', type=int, default=1000, help='Number of Seconds before ending')
    args = parser.parse_args()
    main(args)