import copy
from structures import Modeh
from terms import Atom, Constraint, Fact, Literal, Normal, PlaceMarker
import clingo

class Deduction:
    def __init__(self, delta, EX, MH, MB, BG):
        self.delta = delta
        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG

    def isSubsumed(self, atom: Atom, modeh: Modeh):
        if atom.predicate == modeh.atom.predicate:
            return True
        return False

    def positiveHelper(self, a, m):
        t = set()
        for term1, term2 in zip(a.terms, m.terms):
            if isinstance(term2, Atom):
                t.update(self.positiveHelper(term1, term2))
            elif isinstance(term2, PlaceMarker) and term2.marker == '+':
                t.add((term1.value, term2.type))
            else:
                continue
        return t
    
    def substitute(self, s, a, n): # a starts a copy of s
        nt = set()
        nt.update(n)
        for i in range(len(s.terms)):
            if isinstance(s.terms[i], PlaceMarker) and s.terms[i].marker == '+':
                a.terms += [Normal(nt.pop()[0])]
            elif isinstance(s.terms[i], Atom):
                a.terms += [self.substitute(self, s, a, nt)]
            else:
                a.terms += [s.terms[i]]
                continue
        return a
    
    # ---------- call clingo to generate solutions ----------- #
    def isSatisfiable(self, program):
        control = clingo.Control()
        control.add("base", [], program)
        control.ground([("base", [])])
        models = []
        def on_model(model):
            model = model.symbols(shown=True)
            models.append(model)
        result = control.solve(on_model=on_model)
        isSat = result.satisfiable
        return True if (isSat == True) else False

    def deduce(self, program):
        #A = []
        #T = self.BG + [Fact(d) for d in self.delta]
        k = {}

        # loop through alpha values (subset of delta)
        for alpha in self.delta:

            # find modeh that is subsumed by alpha
            modeh = None
            for m in self.MH:
                if self.isSubsumed(alpha, m):
                    modeh = m
            
            # if no modeh found skip for alpha
            if modeh == None:
                continue

            # get set of positive variables
            n = self.positiveHelper(alpha, modeh.atom)

            # head declaration
            k[alpha] = []

            # iterative expansion
            depth = len(self.MB) # TEMPORARY -> this needs updating
            for d in range(depth):
                # iteratively add constraints and see if satisfiable.
                modeb = self.MB[d]

                # step 1 : extract schema from modeb
                schema_literal = Literal(self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), n), not modeb.negation)
                schema = str(Constraint([schema_literal]))
                types = '\n'.join( [ str(Constraint([Literal(Atom(x[1], [Normal(x[0])]), True)])) for x in n] )
                deltaProgram = '\n'.join([str(Fact(d)) for d in self.delta])
                deductiveProgram = '%DEDUCTIVES \n' + deltaProgram + '\n' + types + '\n' + schema
                query = program + '\n' + deductiveProgram

                # step 2 : add to clingo model, see if terms are allowed.
                #print("\n\n\nQUERY --------------------\n", query)
                isSat = self.isSatisfiable(query)
                #print("SATISFIABLE? ", isSat)

                # step 3 : if terms allowed, add to body of kernel set.
                if isSat:
                    k[alpha] = k[alpha] + [Literal(schema_literal.atom, not schema_literal.negation)]
        for key in k.keys():
            print(f"key : {str(key)}")
            print(f"values : {[str(body) for body in k[key]]}\n")
        






        