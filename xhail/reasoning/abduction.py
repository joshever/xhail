# ----- ABDUCTION PHASE (1) ------- #
# ---------- abductor ----------- #
class Abduction:
    # ---------- examples, modehs, background, model required ----------- #
    def __init__(self, model):
        self.EX = model.EX
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.model = model

    # ---------- methods for constructing program ---------- #
    def loadExamples(self, examples):
        examplesProgram = '%EXAMPLES%\n'
        for example in examples:
            examplesProgram += example.createProgram() + '\n'
        return examplesProgram + '\n'
    
    def loadAbducibles(self, modehs):
        abduciblesProgram = '%ABDUCIBLES%\n'
        for modeh in modehs:
            abduciblesProgram += modeh.createProgram() + '\n'
        return abduciblesProgram + '\n'
    
    def loadNegations(self, modebs):
        negationProgram = '%NEGATIONS%\n'
        for modeb in modebs:
            if modeb.negation == True:
                negationProgram += modeb.createProgram() + '\n'
            else:
                continue
        return negationProgram + '\n'
        
    def loadBackground(self, background):
        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in background]) + '\n'
        return backgroundProgram + '\n'

    # ---------- run the abductive phase ---------- #
    def runPhase(self):
        program = self.model.getProgram()

        program += self.loadBackground(self.BG)
        program += self.loadNegations(self.MB)
        program += self.loadExamples(self.EX)
        program += self.loadAbducibles(self.MH)

        self.model.setProgram(program)
        self.model.call()
        self.model.writeProgram("xhail/output/abduction.lp")