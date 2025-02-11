import ply.lex as lex
import ply.yacc as yacc
from structures import Modeb, Example, Modeh
from terms import Atom, Clause, Constraint, Fact, Literal, Normal, PlaceMarker

# List of tokens
tokens = (
    'EXAMPLE',
    'MODEB',
    'MODEH',
    'PREDICATE',
    'TERM',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'IMPLIES',
    'DOT',
    'NOT',
    'MARKER',
)

# Token definitions
t_EXAMPLE = r'\#example'
t_MODEH = r'\#modeh'
t_MODEB = r'\#modeb'
t_PREDICATE = r'([a-zA-Z_][a-zA-Z_0-9]*)(?=\()'
t_TERM = r'[a-zA-Z_][a-zA-Z_0-9]*|[0-9]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_IMPLIES = r':-'
t_DOT = r'\.'
t_NOT = r'not'
t_MARKER = r'\+|\-|\$'
t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_ignore_COMMENT(t):
    r'%.*'
    pass

lexer = lex.lex()

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
              | rule
              | fact #this is taking precidence
              | constraint
    '''
    p[0] = p[1]

def p_fact(p):
    '''fact : atom DOT'''
    p[0] = Fact(p[1])

def p_constraint(p):
    '''constraint : IMPLIES body DOT'''
    p[0] = Constraint(p[2])

def p_rule(p):
    '''rule : atom IMPLIES body DOT'''
    p[0] = Clause(p[1], p[3])

def p_literal(p):
    '''literal : NOT atom
               | atom
    '''
    p[0] = Literal(p[2], negation=True) if len(p) == 3 else Literal(p[1], negation=False)

def p_atom(p):
    '''atom : PREDICATE LPAREN terms RPAREN'''
    p[0] = Atom(p[1], p[3])

def p_body(p):
    '''body : body COMMA literal
            | literal
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_terms(p):
    '''terms : TERM
             | TERM COMMA terms
             | PREDICATE LPAREN terms RPAREN
             | PREDICATE LPAREN terms RPAREN COMMA terms
    '''
    if len(p) == 2:
        p[0] = [Normal(p[1])]
    elif len(p) == 4:
        p[0] = [Normal(p[1])] + p[3]
    elif len(p) == 5:
        p[0] = [Normal(Atom(p[1], p[3]))]
    else:
        p[0] = [Normal(Atom(p[1], p[3]))] + p[6]


def p_example(p):
    '''example : EXAMPLE atom DOT
               | EXAMPLE NOT atom DOT
    '''
    if len(p) == 4:
        p[0] = Example(p[2], negation=False)
    else:
        p[0] = Example(p[3], negation=True)

# Modeh clause: "#modeh attack(+cat)."
def p_modeh(p):
    '''modeh : MODEH PREDICATE LPAREN MARKER TERM RPAREN DOT'''
    p[0] = Modeh(Atom(p[2], [PlaceMarker(marker=p[4], type=p[5])]), '*')

# Modeb clause: "#modeb predicate(+x)." or "modeb not predicate(-x)"
def p_modeb(p):
    '''modeb : MODEB PREDICATE LPAREN MARKER TERM RPAREN DOT
             | MODEB NOT PREDICATE LPAREN MARKER TERM RPAREN DOT
             '''
    if len(p) == 8:
        p[0] = Modeb(Atom(p[2], [PlaceMarker(p[4], p[5])]), '*', False)
    else:
        p[0] = Modeb(Atom(p[3], [PlaceMarker(p[5], p[6])]), '*', True)
    

def p_error(p):
    if p:
        print(f"Syntax error at {p.value}")
    else:
        print("Syntax error at EOF")

def parseProgram(data):
    parser = yacc.yacc(start='program', debug=True)

    result = parser.parse(data)

    return result
