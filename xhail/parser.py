import ply.lex as lex
import ply.yacc as yacc

# List of tokens
tokens = (
    'KEYWORD',
    'PREDICATE',
    'TERM',
    'LP',
    'RP',
    'COMMA',
    'DOT',
    'NOT',
    'MARKER',
    'COMMENT',
)

# Token definitions
t_KEYWORD = r'\#(example|modeh|modeb)'
t_PREDICATE = r'([a-zA-Z_][a-zA-Z_0-9]*)(?=\()'
t_TERM = r'[a-zA-Z_][a-zA-Z_0-9]*|[0-9]+'
t_LP = r'\('
t_RP = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_NOT = r'not'
t_MARKER = r'\+|\-|\$'
t_COMMENT = r'%.*'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
    '''program : program clause
               | clause'''
    # You can collect the clauses here if needed.
    pass

def p_clause(p):
    '''clause : example
              | modeh
              | modeb'''
    pass

# Example clause: "#example predicate(x, y)."
def p_example(p):
    '''example : KEYWORD PREDICATE LP TERM COMMA TERM RP DOT'''
    print(f"Parsed example: {p[2]}({p[4]}, {p[6]})")
    print(p[0:9])

# Modeh clause: "#modeh attack(+cat)."
def p_modeh(p):
    '''modeh : KEYWORD PREDICATE LP MARKER TERM RP DOT'''
    # p[2]: predicate, p[4]: marker, p[5]: term
    print(f"Parsed modeh: {p[2]}({p[4]}{p[5]})")
    print(p)

# Modeb clause: "#modeb predicate(x)."
def p_modeb(p):
    '''modeb : KEYWORD PREDICATE LP TERM RP DOT'''
    print(f"Parsed modeb: {p[2]}({p[4]})")
    print(p)

def p_error(p):
    if p:
        print(f"Syntax error at {p.value}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(start='program')

data = "#example predicate(x, y). #example predicate(x, y). #modeh attack(+cat)."

lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type}: {tok.value}")

parser.parse(data)
