import ply.lex as lex
import ply.yacc as yacc
from ..language.structures import Modeb, Example, Modeh
from ..language.terms import Atom, Clause, Constraint, Fact, Literal, Normal, PlaceMarker

# ---------- prepare tokens ----------- #
tokens = (
    'NOT',
    'EXAMPLE_KEY',
    'MODEB_KEY',
    'MODEH_KEY',
    'PREDICATE',
    'TERM',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'IMPLIES',
    'DOT',
    'MARKER',
    'OPERATOR',
)

# ---------- define tokens ----------- #
t_NOT = r'(?<!\S)not(?!\S)'
t_EXAMPLE_KEY = r'\#example'
t_MODEH_KEY = r'\#modeh'
t_MODEB_KEY = r'\#modeb'
t_PREDICATE = r'(?!not\b)([a-zA-Z_][a-zA-Z_0-9]*)(?=\()'
t_TERM = r'(?!not\b)[a-zA-Z_][a-zA-Z_0-9]*|[0-9]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_IMPLIES = r':-'
t_DOT = r'\.'
t_MARKER = r'\+|\-|\$'
t_OPERATOR = r'(==|!=|<=|>=|<|>)'
t_ignore = ' \t\n'

# ---------- special tokens ----------- #
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_ignore_COMMENT(t):
    r'%.*'
    pass

lexer = lex.lex()

# ---------- program and clauses ---------- #
def p_program(p):
    '''program : program clause
               | clause'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_clause(p):
    '''clause : example
              | modeb
              | modeh
              | fact
              | normal_clause
              | constraint
    '''
    p[0] = p[1]


# ---------- atom ---------- #
def p_atom(p):
    '''atom : PREDICATE LPAREN terms RPAREN
    '''
    p[0] = Atom(p[1], p[3])

# ---------- schema ---------- #
def p_schema(p):
    '''schema : PREDICATE LPAREN schema_terms RPAREN'''
    p[0] = Atom(p[1], p[3])

def p_schema_terms(p):
    '''schema_terms : MARKER TERM
                    | MARKER TERM COMMA schema_terms
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
        
# ---------- example ---------- #
def p_example(p):
    '''example : EXAMPLE_KEY atom DOT
               | EXAMPLE_KEY NOT atom DOT
    '''
    if len(p) == 4:
        p[0] = Example(p[2], negation=False)
    else:
        p[0] = Example(p[3], negation=True)

# ---------- modeh ---------- #
def p_modeh(p):
    '''modeh : MODEH_KEY schema DOT'''
    p[0] = Modeh(p[2], '*')

# ---------- modeb ---------- #
def p_modeb(p):
    '''modeb : MODEB_KEY schema DOT
             | MODEB_KEY NOT schema DOT
             '''
    if len(p) == 4:
        p[0] = Modeb(p[2], '*', False)
    else:
        p[0] = Modeb(p[3], '*', True)

# ---------- terms ---------- #
def p_terms(p):
    '''terms : TERM
             | atom
             | TERM COMMA terms
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

# ---------- fact ---------- #
def p_fact(p):
    '''fact : atom DOT
    '''
    p[0] = Fact(p[1])

# ---------- contraint ---------- #
def p_constraint(p):
    '''constraint : NOT body DOT
    '''
    p[0] = Constraint(p[2], True)

# ---------- normal_clause ---------- #
def p_normal_clause(p):
    '''normal_clause : atom IMPLIES body DOT
    '''
    p[0] = Clause(p[1], p[3])

def p_body(p):
    '''body : literal COMMA body
            | literal
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

def p_literal(p):
    '''literal : NOT atom
               | atom
               | TERM OPERATOR TERM
    '''
    if len(p) == 2:
        p[0] = [Literal(p[1], False)]
    else:
        p[0] = [Literal(p[2], True)]

# ---------- error ---------- #
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

class Parser:
    data = ""
    parsedData = []
    
    def __init__(self):
        return

    # ---------- string -> Example | Modeh | Modeb | Background ---------- #
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

    # ---------- default parse mode ----------- #
    def parseProgram(self):
        parser = yacc.yacc(debug=True, start='program')
        self.parsedData = parser.parse(self.data)
        return self.parsedData

    # ---------- debug parse mode ----------- #
    def tokenByToken(self):
        lexer = lex.lex()
        lexer.input(self.data)
        for token in lexer:
            print(f"Token type: {token.type}, Token value: {token.value}")

    def loadFile(self, filename):
        path = f'{filename}'
        file = open(path, 'r', encoding="utf-8")
        self.data = file.read()
        file.close()
        return self.data
    
    def loadString(self, str):
        self.data = str

