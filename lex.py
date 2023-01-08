 
import ply.lex as lex

reserved = {
    'print-num': 'print_num',
    'print-bool': 'print_bool',
    'mod': 'mod',
    'and': 'and',
    'or': 'or',
    'not': 'not',
    'define': 'define',
    'if': 'if_',
    'fun': 'fun_'
}

tokens = [
    'id','number','bool_', 
    'plus', 'minus', 'mul', 'div', 'equal', 
    'lpr', 'rpr', 'greater', 'smaller'
    ] + list(reserved.values())
 
# literals = ['=','+','-','*','/', '(',')']
 
# Tokens
t_plus  = r'\+'
t_minus = r'-'
t_mul = r'\*'
t_div = r'/'
t_equal = r'='
t_lpr  = r'\('
t_rpr  = r'\)'
t_greater = r'>'
t_smaller = r'<'
 
def t_id(t):
    r'[a-z]([a-z]|[0-9]|\-)*'
    t.type = reserved.get(t.value, 'id')    # Check for reserved words
    return t

def t_number(t):
    r'0|[1-9][0-9]*|\-[1-9][0-9]*'
    t.value = int(t.value)
    return t

def t_bool_(t):
    r'\#t|\#f'
    if t.value == "#t":
        t.value = True
    else:
        t.value = False
    return t
 
t_ignore = " \t"
 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
lexer = lex.lex()

# import os, sys

# if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
#     data = open(sys.argv[1]).read()
#     lexer.input(data)
#     while True:
#         tok = lexer.token()
#         if not tok: 
#             break      # No more input
#         print(tok)
