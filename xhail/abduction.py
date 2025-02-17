# ----- ABDUCTION PHASE (1) ------- #
# ---------- abductor ----------- #
class Abduction:
    # ---------- examples, modehs, background, model required ----------- #
    def __init__(self, model):
        self.EX = model.EX
        self.MH = model.MH
        self.BG = model.BG
        self.model = model

    # ---------- run the abductive phase ---------- #
    def runPhase(self):
        self.model.loadBackground(self.BG)
        self.model.loadExamples(self.EX)
        self.model.loadAbducibles(self.MH)
        self.model.call()
        self.model.writeProgram()