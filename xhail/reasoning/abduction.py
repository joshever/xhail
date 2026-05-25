# ----- ABDUCTION PHASE (1) ------- #
import logging

logger = logging.getLogger(__name__)

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
            if modeb.negation:
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
        logger.debug("Running abduction phase...")
        self.model.call()

        if self.model.debug_output_dir is not None:
            dest = self.model.debug_output_dir / "abduction.lp"
            dest.parent.mkdir(parents=True, exist_ok=True)
            self.model.writeProgram(str(dest))
            logger.debug("Abduction program written to %s", dest)
