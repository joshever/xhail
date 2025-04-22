from xhail.reasoning.abduction import Abduction
from xhail.reasoning.deduction import Deduction
from xhail.reasoning.induction import Induction
from xhail.reasoning.model import Model
from xhail.parser.parser import Parser

if __name__ == '__main__':
    # ---------- read input ---------- #
    DEPTH = 3
    INPUT_FILENAME = 'tests/out_bug.lp'#'example1.lp'#'tests/deduction.lp'#'test.lp'#

    # ---------- parse data ---------- #
    parser = Parser()
    parser.loadFile(INPUT_FILENAME)
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate()

    # # print my program
    # for ex in EX:
    #     print(str(ex))

    # for mh in MH:
    #     print(str(mh))

    # for mb in MB:
    #     print(str(mb))
    
    # for bg in BG:
    #     print(str(bg))
    
    

    # create empty context Model
    model = Model(EX, MH, MB, BG, DEPTH)
    # IF HYPOTHESIS == [] -> REPEAT UNTIL MODEH MIN == MODEH MAX OR ABDUCTION UNSATISFIED.
    
    abduction, deduction, induction = Abduction(model), Deduction(model), Induction(model)
    
    abduction.runPhase()
    deduction.runPhase()
    induction.runPhase()
    
    print("deltas:", [str(d) for d in model.getDelta()])
    print("kernel:", [str(k) for k in model.getKernel()])
    print("hypothesis:", [str(h) for h in model.getHypothesis()])