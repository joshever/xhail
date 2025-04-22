# -------------------------------------- #
# ---------- ABDUCTION CLASS ----------- #
# -------------------------------------- #

class Abduction:
    # ----- examples, modehs, background, context required ------ #
    def __init__(self, context):
        self.EX = context.EX
        self.MH = context.MH
        self.MB = context.MB
        self.BG = context.BG
        self.context = context

    # ---------- INCREASE ABDUCIBLES COUNT ---------- #
    def incrementMax(self):
        valid = False
        for mh in self.MH:
            if mh.getMin() < mh.getMax():
                mh.setMin(mh.getMin() + 1)
                valid = True
        return valid

    # ---------- LOAD METHODS ---------- #
    def loadExamples(self, examples):
        examplesProgram = '%EXAMPLES%\n'
        for example in examples:
            examplesProgram += '%' + str(example) + '\n'
            examplesProgram += example.createProgram() + '\n'
        return examplesProgram + '\n'
    
    def loadAbducibles(self, modehs):
        abduciblesProgram = '%ABDUCIBLES%\n'
        for modeh in modehs:
            abduciblesProgram += '%' + str(modeh) + '\n'
            abduciblesProgram += modeh.createProgram() + '\n'
        return abduciblesProgram + '\n'
    
    def loadNegations(self, modebs):
        negationProgram = '%TEMPORARY NEGATIONS%\n'
        for modeb in modebs:
            if modeb.negation == True:
                negationProgram += modeb.createProgram() + '\n'
            else:
                continue
        return negationProgram + '\n'

    def loadBackground(self, background):
        backgroundProgram = '%ORIGINAL BACKGROUND%\n' + '\n'.join([str(b) for b in background]) + '\n'
        return backgroundProgram + '\n'

    # ---------- RUN ---------- #
    def run(self):
        program = ""

        program += self.loadBackground(self.BG)
        program += self.loadNegations(self.MB)
        program += self.loadExamples(self.EX)
        program += self.loadAbducibles(self.MH)

        abd_id = self.context.addInterface(program) # 5 second timeout
        self.context.current_id = abd_id
        self.context.writeInterfaceProgram(abd_id, "xhail/output/abduction.lp")
        self.context.loadDelta(abd_id)