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
    def incrementMin(self):
        valid = False
        new_MH = []
        for mh in self.MH:
            if int(mh.getMin()) < int(mh.getMax()):
                mh.setMin(int(mh.getMin()) + 1)
                valid = True
            new_MH.append(mh)
        self.MH = new_MH
        self.context.MH = new_MH
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
    
    def loadProgram(self):
        program = ""
        program += self.loadBackground(self.BG)
        program += self.loadNegations(self.MB)
        program += self.loadExamples(self.EX)
        program += self.loadAbducibles(self.MH)
        return program
    
    def callInterface(self, program):
        abd_id = self.context.addInterface(program) # 5 second timeout
        self.context.current_id = abd_id
        self.context.writeInterfaceProgram(abd_id, "xhail/output/abduction.lp")
        self.context.loadDelta(abd_id)
        self.abd_id = abd_id
        

    # ---------- RUN ---------- #
    def run(self):
        #self.context.delta = []
        #while self.context.delta == []:
        #self.context.current_id = self.abd_id
        program = self.loadProgram()
        self.callInterface(program)
            # else:
            #     res = self.context.interfaces[self.abd_id].getNextModel()
            #     # more models with this program?
            #     if res != None:
            #         self.context.loadDelta(self.abd_id)
            #     # update program
            #     else:
            #         res = self.incrementMin()
            #         # if no result. set to stop
            #         if res == None:
            #             self.context.setState('UNSATISFIABLE')
            #         # update min.
            #         else:
            #             program = self.loadProgram()
            #             self.context.interfaces[self.abd_id].setProgram(program)
            #             self.context.interfaces[self.abd_id].loadBestModel()
            #             self.context.writeInterfaceProgram(self.abd_id, "xhail/output/abduction.lp")
            #             self.context.loadDelta(self.abd_id)
        
            