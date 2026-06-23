# ----- ABDUCTION PHASE (1) ------- #
import logging

from .utils import load_background, load_examples

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

    def loadAbducibles(self, modehs):
        abduciblesProgram = "%ABDUCIBLES%\n"
        for modeh in modehs:
            abduciblesProgram += modeh.createProgram() + "\n"
        return abduciblesProgram + "\n"

    def loadNegations(self, modebs):
        negationProgram = "%NEGATIONS%\n"
        for modeb in modebs:
            if modeb.negation:
                negationProgram += modeb.createProgram() + "\n"
        return negationProgram + "\n"

    # ---------- run the abductive phase ---------- #
    def runPhase(self):
        program = self.model.getProgram()

        program += load_background(self.BG)
        program += self.loadNegations(self.MB)
        program += load_examples(self.EX)
        program += self.loadAbducibles(self.MH)

        self.model.setProgram(program)
        logger.debug("Running abduction phase...")
        self.model.call()

        if self.model.debug_output_dir is not None:
            dest = self.model.debug_output_dir / "abduction.lp"
            dest.parent.mkdir(parents=True, exist_ok=True)
            self.model.writeProgram(str(dest))
            logger.debug("Abduction program written to %s", dest)
