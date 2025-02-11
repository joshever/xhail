import ply.lex as lex
import ply.yacc as yacc
from structures import Modeb, Example, Modeh
from terms import Atom, Normal, PlaceMarker

# List of tokens
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
)

# Token definitions
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
t_ignore = ' \t\n'

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
    '''
    p[0] = p[1]


# ---------- atom ---------- #
def p_atom(p):
    '''atom : PREDICATE LPAREN terms RPAREN'''
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

# ---------- error ---------- #
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

def parseProgram(data):
    parser = yacc.yacc(debug=True, start='program')
    result = parser.parse(data)
    return result

if __name__ == '__main__':
    my_program = """
    #modeb not cars(mole(+cat, -badger), +cat).
    #modeh bright(-right).
    #example car(car(yes)).
    """
    result = parseProgram(my_program)
    for item in result:
        if isinstance(item, Example):
            print(str(item))
        elif isinstance(item, Modeb):
            print(str(item))
        elif isinstance(item, Modeh):
            print(str(item))
        


    # lexer = lex.lex()

    # # Input string to be processed
    # input_string = """
    # #modeb not cars(+mole).
    # """

    # # Pass the input string to the lexer
    # lexer.input(input_string)

    # # Iterate through all tokens and print them
    # for token in lexer:
    #     print(f"Token type: {token.type}, Token value: {token.value}")

