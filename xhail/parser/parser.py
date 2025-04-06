import ply.lex as lex
import ply.yacc as yacc
from ..language.structures import Modeb, Example, Modeh
from ..language.terms import Atom, Clause, Constraint, Fact, Literal, MiscLiteral, Normal, PlaceMarker

# ----------------------------------- #
# ---------- DEFINE LEXER ----------- #
# ----------------------------------- #

tokens = (
    'NOT',
    'EXAMPLE_KEY',
    'MODEB_KEY',
    'MODEH_KEY',
    'PREDICATE',
    #'term',
    'UPPER',
    'LOWER',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'IMPLIES',
    'DOT',
    'MARKER',
    'OPERATOR',
    'MIN',
    'MAX',
    'WEIGHT',
    'PRIORITY',
)

# Define Tokens
t_NOT = r'(?<!\S)not(?!\S)'
t_EXAMPLE_KEY = r'\#example'
t_MODEH_KEY = r'\#modeh'
t_MODEB_KEY = r'\#modeb'
t_PREDICATE = r'(?!not\b)([a-z][a-zA-Z_0-9]*)(?=\()'
#t_ZERO_PREDICATE = r'(?!not\b)([a-z][a-zA-Z_0-9]*)'
#t_TERM = r'(?!not\b)[a-zA-Z_][a-zA-Z_0-9]*|[0-9]+'
t_UPPER = r'(?!not\b)\b[A-Z][a-zA-Z0-9_]*\b'
t_LOWER = r'(?!not\b)\b[a-z][a-zA-Z0-9_]*\b'
t_NUMBER = r'\d'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_IMPLIES = r':-'
t_DOT = r'\.'
t_MARKER = r'\+|\-|\$'
t_OPERATOR = r'(==|!=|<=|>=|<|>)'
t_MIN = r'\~'
t_MAX = r':'
t_WEIGHT = r'='
t_PRIORITY = r'@'
t_ignore = ' \t\n'

# ----- Special Tokens ----- #
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_ignore_COMMENT(t):
    r'%.*'
    pass

lexer = lex.lex()

# ----------------------------------------- #
# ---------- PARSER EXPRESSIONS ----------- #
# ----------------------------------------- #

# ----- base text ----- #

def p_term(p):
    '''term : LOWER
            | NUMBER
            | UPPER
    '''
    p[0] = p[1]

def p_zero_predicate(p):
    '''zero_predicate : LOWER'''
    p[0] = Atom(p[1], [])

# ----- program definition ----- #
def p_program(p):
    '''program : program clause
               | clause'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# ----- clause definition ----- #
def p_clause(p):
    '''clause : example
              | modeb
              | modeh
              | fact
              | normal_clause
              | constraint
    '''
    p[0] = p[1]

# ----- atom definition ----- #
def p_atom(p):
    '''atom : PREDICATE LPAREN terms RPAREN
    '''
    p[0] = Atom(p[1], p[3])

# ----- schema definition ----- #
def p_schema(p):
    '''schema : PREDICATE LPAREN schema_terms RPAREN
    '''
    p[0] = Atom(p[1], p[3])

# ----- schema terms definition ----- #
def p_schema_terms(p):
    '''schema_terms : MARKER term
                    | MARKER term COMMA schema_terms
                    | schema
                    | schema COMMA schema_terms
    '''
    if len(p) == 3:
        p[0] = [PlaceMarker(marker=p[1], type=p[2])]
    elif len(p) == 5:
        p[0] = [PlaceMarker(marker=p[1], type=p[2])] + p[4]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# ----- min max constraints definition ----- #
def p_min_max_bias(p):
    '''min_max_bias : MAX term MIN term
                    | MAX term
    '''
    if len(p) == 3:
        p[0] = {'max': p[2]}
    else:
        p[0] = {'min': p[2], 'max': p[4]}

# ----- priority bias definition ----- #
def p_priority_bias(p):
    '''priority_bias : PRIORITY term'''
    p[0] = {'priority': p[2]}

# ----- weight bias definition ----- #
def p_weight_bias(p):
    '''weight_bias : WEIGHT term'''
    p[0] = {'weight': p[2]}

# ----- bias definition ----- #
def p_bias(p):
    '''bias : min_max_bias weight_bias priority_bias
            | min_max_bias priority_bias
            | min_max_bias weight_bias
            | weight_bias priority_bias
            | weight_bias
            | priority_bias
            | min_max_bias
    '''
    values = {}
    for i in range(1, len(p[1:])):
        if 'min' in p[i].keys():
            values['min'] = p[i]['min']
        if 'max' in p[i].keys():
            values['max'] = p[i]['max']
        if 'priority' in p[i].keys():
            values['priority'] = p[i]['priority']
        if 'weight' in p[i].keys():
            values['weight'] = p[i]['weight']
    p[0] = values
        
# ----- example definition ----- #
def p_example(p):
    '''example : EXAMPLE_KEY atom DOT
               | EXAMPLE_KEY NOT atom DOT
               | EXAMPLE_KEY atom bias DOT
               | EXAMPLE_KEY NOT atom bias DOT
               | EXAMPLE_KEY zero_predicate DOT
               | EXAMPLE_KEY NOT zero_predicate DOT
               | EXAMPLE_KEY zero_predicate bias DOT
               | EXAMPLE_KEY NOT zero_predicate bias DOT
    '''
    if len(p) == 4: # just atom
        p[0] = Example(p[2], negation=False)
    elif len(p) == 6: # negated and biased
        new_example = Example(p[3], negation=True)
        if 'weight' in p[4].keys():
            new_example.setWeight(p[4]['weight'])
        if 'priority' in p[4].keys():
            new_example.setPriority(p[4]['priority'])
        p[0] = new_example

    elif len(p) == 5 and isinstance(p[3], Atom):
        p[0] = Example(p[3], negation=True)
    else:
        new_example = Example(p[2], negation=False)
        if 'weight' in p[3].keys():
            new_example.setWeight(p[3]['weight'])
        if 'priority' in p[3].keys():
            new_example.setPriority(p[3]['priority'])
        p[0] = new_example    

# ----- modeh definition ----- #
def p_modeh(p):
    '''modeh : MODEH_KEY schema DOT
             | MODEH_KEY schema bias DOT
             | MODEH_KEY zero_predicate DOT
             | MODEH_KEY zero_predicate bias DOT
    '''
    if len(p) == 4:
        p[0] = Modeh(p[2], '*')
    else:
        modeh = Modeh(p[2], '*')
        if 'min' in p[3].keys():
            modeh.setMin(p[3]['min'])
        if 'max' in p[3].keys():
            modeh.setMax(p[3]['max'])
        if 'weight' in p[3].keys():
            modeh.setWeight(p[3]['weight'])
        if 'priority' in p[3].keys():
            modeh.setPriority(p[3]['priority'])
        p[0] = modeh

# ----- modeb definition ----- #
def p_modeb(p):
    '''modeb : MODEB_KEY schema DOT
             | MODEB_KEY NOT schema DOT
             | MODEB_KEY schema bias DOT
             | MODEB_KEY NOT schema bias DOT
             | MODEB_KEY zero_predicate DOT
             | MODEB_KEY NOT zero_predicate DOT
             | MODEB_KEY zero_predicate bias DOT
             | MODEB_KEY NOT zero_predicate bias DOT
             '''
    if len(p) == 4:
        p[0] = Modeb(p[2], '*', False)
    elif len(p) == 6:
        modeb = Modeb(p[3], '*', True)
        if 'max' in p[4].keys():
            modeb.setMax(p[4]['max'])
        if 'weight' in p[4].keys():
            modeb.setWeight(p[4]['weight'])
        if 'priority' in p[4].keys():
            modeb.setPriority(p[4]['priority'])
        p[0] = modeb
    elif len(p) == 5 and isinstance(p[3], Atom):
        p[0] = Modeb(p[3], '*', True)
    else:
        modeb = Modeb(p[2], '*', False)
        if 'max' in p[3].keys():
            modeb.setMax(p[3]['max'])
        if 'weight' in p[3].keys():
            modeb.setWeight(p[3]['weight'])
        if 'priority' in p[3].keys():
            modeb.setPriority(p[3]['priority'])
        p[0] = modeb
        
# ----- terms definition ----- #
def p_terms(p):
    '''terms : term
             | atom
             | term COMMA terms
             | atom COMMA terms
    '''
    if len(p) == 2 and not isinstance(p[1], Atom):
        p[0] = [Normal(p[1])]
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4 and not isinstance(p[1], Atom):
        p[0] = [Normal(p[1])] + p[3]
    else:
        p[0] = [p[1]] + p[3]

# ----- fact definition ----- #
def p_fact(p):
    '''fact : atom DOT
            | zero_predicate DOT
    '''
    p[0] = Fact(p[1])

# ----- constraint definition ----- #
def p_constraint(p):
    '''constraint : IMPLIES body DOT
    '''
    p[0] = Constraint(p[2])

# ----- normal clause definition ----- #
def p_normal_clause(p):
    '''normal_clause : atom IMPLIES body DOT
                     | zero_predicate IMPLIES body DOT
    '''
    p[0] = Clause(p[1], p[3])

# ----- body definition ----- #
def p_body(p):
    '''body : literal COMMA body
            | literal
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

# ----- literal definition ----- #
def p_literal(p):
    '''literal : NOT atom
               | atom
               | term OPERATOR term
               | NOT term OPERATOR term
               | NOT zero_predicate
               | zero_predicate
    '''
    if len(p) == 2:
        p[0] = [Literal(p[1], False)]
    elif len(p) == 4:
        val = p[1] + p[2] + p[3]
        p[0] = [MiscLiteral(val, False)]
    elif len(p) == 5:
        val = p[2] + p[3] + p[4]
        p[0] = [MiscLiteral(val, True)]
    else:
        p[0] = [Literal(p[2], True)]

# ----- error definition ----- #
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

# ----------------------------------- #
# ---------- PARSER CLASS ----------- #
# ----------------------------------- #

class Parser:
    data = ""
    parsedData = []
    
    def __init__(self):
        return

    # ----- string -> Example | Modeh | Modeb | Background ----- #
    def separate(self):
        examples = []
        modehs = []
        modebs = []
        background = []
        for item in self.parsedData:
            if isinstance(item, Example):
                examples.append(item)
            elif isinstance(item, Modeb):
                modebs.append(item)
            elif isinstance(item, Modeh):
                modehs.append(item)
            elif isinstance(item, Clause):
                background.append(item)
        return examples, modehs, modebs, background

    # ----- default parse mode ----- #
    def parseProgram(self):
        parser = yacc.yacc(debug=True, start='program')
        self.parsedData = parser.parse(self.data)
        return self.parsedData

    # ----- debug parse mode ----- #
    def tokenByToken(self):
        lexer = lex.lex()
        lexer.input(self.data)
        for token in lexer:
            print(f"Token type: {token.type}, Token value: {token.value}")

    # ----- load file given filename ----- #
    def loadFile(self, filename):
        path = f'{filename}'
        file = open(path, 'r', encoding="utf-8")
        self.data = file.read()
        file.close()
        return self.data
    
    # ----- load given string ----- #
    def loadString(self, str):
        self.data = str

