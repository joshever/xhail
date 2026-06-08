import logging
import os
from pathlib import Path
from typing import Optional

import clingo

from ..language.terms import Atom, Fact, Normal, PlaceMarker

logger = logging.getLogger(__name__)

class Model:
    def __init__(
        self,
        EX: list,
        MH: list,
        MB: list,
        BG: list,
        DEPTH: int,
        debug_output_dir: Optional[Path] = None,
    ):
        # D10 fix: these were class attributes, meaning state was shared across all Model instances
        # in the same process. They are now instance attributes.
        self.program = ""
        self.clingo_models = []
        self.best_model = None
        self.delta = []
        self.kernel: list = []       # clauses built during deduction
        self.hypothesis: list = []   # final learned clauses set by induction
        self._subsumption_cache: dict = {}  # (str(atom), str(mode)) -> bool

        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG
        self.DEPTH = DEPTH
        # If set, abduction and induction write intermediate ASP programs here.
        self.debug_output_dir: Optional[Path] = debug_output_dir

    # ---------- METHODS ---------- #
    def call(self):
        control = clingo.Control()
        control.add("base", [], self.program)
        control.ground([("base", [])])
        clingo_models = []
        def on_model(clingo_model):
            clingo_model = clingo_model.symbols(shown=True)
            clingo_models.append(clingo_model)
        control.solve(on_model=on_model)
        self.clingo_models = clingo_models
        return clingo_models

    def getBestModel(self):
        n_threads = min(4, os.cpu_count() or 1)
        control = clingo.Control([f"--parallel-mode={n_threads}"])
        control.add("base", [], self.program)
        control.ground([("base", [])])
        clingo_models = []

        def on_model(clingo_model):
            model_symbols = clingo_model.symbols(shown=True)
            model_cost = clingo_model.cost
            logger.debug("clingo model: %s  cost: %s", model_symbols, model_cost)
            clingo_models.append([model_symbols, model_cost])

        control.solve(on_model=on_model)
        #result = handle.get()  # Wait for the solving process to finish
        #if not clingo_models:
        #    return None
        if clingo_models == []:
            return '[]'
        # Select the best model based on lexicographical order of the cost vector
        best_model = min(clingo_models, key=lambda m: [int(c) for c in m[1]])
        self.best_model = best_model
        return best_model[0]


    def writeProgram(self, destination):
        file = open(destination, "w")
        file.write(self.program)
        file.close()

    def clearProgram(self):
        self.program = ""

    # ensures normal values are the same, and any placeholders can be different.
    def isSubsumed(self, atom, mode) -> bool:
        cache_key = (str(atom), str(mode))
        if cache_key in self._subsumption_cache:
            return self._subsumption_cache[cache_key]
        result = self._isSubsumed(atom, mode)
        self._subsumption_cache[cache_key] = result
        return result

    def _isSubsumed(self, atom, mode) -> bool:
        if atom.predicate != mode.predicate:
            return False
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               if not self.isSubsumed(term1, term2):
                   return False
            elif isinstance(term2, Normal):
                if term1.value != term2.value:
                    return False
            elif isinstance(term2, PlaceMarker) and isinstance(term1, Normal):
                if self.getMatches([Atom(term2.type, [term1])]) == []:
                    return False
                else:
                    continue
            else:
                continue
        return True

    # ---------- clingo Symbol → XHAIL term/fact conversion ---------- #

    def _symbol_to_term(self, symbol) -> "Atom | Normal":
        """Convert a ground clingo Symbol to an XHAIL term (Atom or Normal)."""
        if symbol.type == clingo.SymbolType.Number:
            return Normal(str(symbol.number))
        if symbol.arguments:          # nested functor, e.g. bird(tweety)
            return self._symbol_to_atom(symbol)
        return Normal(symbol.name)    # ground constant, e.g. tweety

    def _symbol_to_atom(self, symbol) -> Atom:
        """Convert a functor clingo Symbol to an XHAIL Atom."""
        return Atom(symbol.name, [self._symbol_to_term(a) for a in symbol.arguments])

    def parseModel(self, model) -> list:
        """Convert a list of ground clingo Symbols to XHAIL Fact objects.

        Replaces the previous implementation which converted symbols to strings
        and re-parsed them with PLY — an unnecessary round-trip that dominated
        runtime on any non-trivial input.
        """
        return [Fact(self._symbol_to_atom(sym)) for sym in model]

    # ---------- GETTERS ---------- #

    def getProgram(self):
        return self.program

    def getClingoModels(self):
        return self.clingo_models

    def getDelta(self):
        head_atoms = [mh.atom for mh in self.MH]
        self.delta = self.getMatches(head_atoms)
        return self.delta

    def getMatches(self, atomConditions):
        # D7 fix: was getClingoModels()[0] which raises IndexError on UNSAT (no models).
        models = self.getClingoModels()
        if not models:
            raise RuntimeError(
                "Abduction yielded no model (program is UNSAT): "
                "no minimal explanation exists for the given examples and background. "
                "Check that the modeh declarations cover the positive examples."
            )
        model = models[0]
        facts = self.parseModel(model)

        result = []
        for fact in facts:
            for mh in atomConditions:
                if self.isSubsumed(fact.head, mh):
                    result.append(fact.head)
        return result

    def getKernel(self):
        return self.kernel

    # ---------- SETTERS ---------- #

    def setKernel(self, kernel):
        self.kernel = kernel

    def setHypothesis(self, clauses: list) -> None:
        """Store the final learned hypothesis (set by the induction phase)."""
        self.hypothesis = clauses

    def getHypothesis(self) -> list:
        """Return the learned hypothesis clauses."""
        return self.hypothesis

    def setProgram(self, program):
        self.program = program

    def getExamples(self):
        return self.EX

    def getBackground(self):
        return self.BG

