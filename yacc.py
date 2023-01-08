# Yacc example

'''
PROGRAM ::= STMT+
STMT ::= EXP | DEF-STMT | PRINT-STMT
PRINT-STMT ::= (print-num EXP) | (print-bool EXP)
EXP ::= bool-val | number | VARIABLE | NUM-OP | LOGICAL-OP
| FUN-EXP | FUN-CALL | IF-EXP
NUM-OP ::= PLUS | MINUS | MULTIPLY | DIVIDE | MODULUS | GREATER
| SMALLER | EQUAL
PLUS ::= (+ EXP EXP+)
MINUS ::= (- EXP EXP)
MULTIPLY ::= (* EXP EXP+)
DIVIDE ::= (/ EXP EXP)
MODULUS ::= (mod EXP EXP)
GREATER ::= (> EXP EXP)
SMALLER ::= (< EXP EXP)
EQUAL ::= (= EXP EXP+)
LOGICAL-OP ::= AND-OP | OR-OP | NOT-OP
AND-OP ::= (and EXP EXP+)
OR-OP ::= (or EXP EXP+)
NOT-OP ::= (not EXP)
DEF-STMT ::= (define VARIABLE EXP)
VARIABLE ::= id
FUN-EXP ::= (fun FUN_IDs FUN-BODY)
FUN-IDs ::= (id*)
FUN-BODY ::= EXP
FUN-CALL ::= (FUN-EXP PARAM*) | (FUN-NAME PARAM*)
PARAM ::= EXP
LAST-EXP ::= EXP
FUN-NAME ::= id
IF-EXP ::= (if TEST-EXP THAN-EXP ELSE-EXP)
TEST-EXP ::= EXP
THEN-EXP ::= EXP
ELSE-EXP ::= EXP
'''

import ply.yacc as yacc
# Get the token map from the lexer. This is required.
from lex import tokens
# import lex

define_var = {}

def p_PROGRAM(p):
    'PROGRAM : STMT_PLUS'
    # print("program: ", p[1])
    p[0] = p[1]

def p_STMT_PLUS(p):
    '''STMT_PLUS    : STMT
                    | STMT STMT_PLUS'''
    # print("stmts: ", p[1])
    p[0] = p[1]

def p_STMT(p):
    '''STMT : EXP 
            | DEF_STMT
            | PRINT_STMT'''
    # print("stmt: ", p[1])
    p[0] = p[1]

def p_PRINT_STMT(p):
    '''PRINT_STMT : lpr print_num EXP rpr
                  | lpr print_bool EXP rpr'''
    if p[2] == 'print-num':
        print(p[3])
    else:
        if bool(p[3]):
            print("#t")
        else:
            print("#f")
        # print(bool(p[3]))

# def p_EXP_PLUS(p):
#     '''EXP_PLUS : EXP
#                 | EXP EXP_PLUS'''
#     # print("exps: ", p[1], p.lexpos(1))
#     p[0] = p[1]

def p_EXP(p):
    '''EXP : bool_
           | number
           | VARIABLE
           | NUM_OP
           | LOGICAL_OP
           | FUN_EXP
           | FUN_CALL
           | IF_EXP'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = p[1]

# def p_bool_val(p):
#     '''bool_val : BOOL'''
#     # print("bool_val: ", p[1])
#     p[0] = p[1]

# def p_number(p):
#     '''number : NUMBER'''
#     # print("number: ", p[1])
#     p[0] = p[1]

def p_NUM_OP(p):
    '''NUM_OP   : PLUS
                | MINUS
                | MULTIPLY
                | DIVIDE
                | MODULUS
                | GREATER
                | SMALLER
                | EQUAL'''
    # print("num_op: ", p[1])
    p[0] = p[1]

def p_PLUS(p):
    '''PLUS : lpr plus EXP PLUS_EXP_PLUS rpr'''
    # print("plus: ", p[3] + p[4])
    p[0] = p[3] + p[4]

def p_PLUS_EXP_PLUS(p):
    '''PLUS_EXP_PLUS    : EXP
                        | EXP PLUS_EXP_PLUS'''
    # print("plusexps: ", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_MINUS(p):
    '''MINUS : lpr minus EXP EXP rpr'''
    # print("minus: ", p[3] - p[4])
    p[0] = p[3] - p[4]

def p_MULTIPLY(p):
    '''MULTIPLY : lpr mul EXP MUL_EXP_PLUS rpr'''
    # print("multiply: ", p[3] * p[4])
    p[0] = p[3] * p[4]

def p_MUL_EXP_PLUS(p):
    '''MUL_EXP_PLUS : EXP
                    | EXP MUL_EXP_PLUS'''
    # print("mul_exps: ", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] * p[2]

def p_DIVIDE(p):
    '''DIVIDE : lpr div EXP EXP rpr'''
    # print("DIVIDE: ", p[3] // p[4])
    p[0] = p[3] // p[4]

def p_MODULUS(p):
    '''MODULUS : lpr mod EXP EXP rpr'''
    # print("MODULUS: ", p[3] % p[4])
    p[0] = p[3] % p[4]

def p_GREATER(p):
    '''GREATER : lpr greater EXP EXP rpr'''
    # print("GREATER: ", p[3] > p[4])
    p[0] = p[3] > p[4]

def p_SMALLER(p):
    '''SMALLER : lpr smaller EXP EXP rpr'''
    # print("SMALLER: ", p[3] < p[4])
    p[0] = p[3] < p[4]

def p_EQUAL(p):
    '''EQUAL : lpr equal EXP EQUAL_EXP_PLUS rpr'''
    # print("EQUAL: ", p[3] == p[4])
    p[0] = p[3] == p[4]

def p_EQUAL_EXP_PLUS(p):
    '''EQUAL_EXP_PLUS   : EXP
                        | EXP EQUAL_EXP_PLUS'''
    # print("EQUAL_EXP_PLUS: ", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] == p[2]

def p_LOGICAL_OP(p):
    '''LOGICAL_OP : AND_OP
                  | OR_OP
                  | NOT_OP'''
    # print("LOGICAL_OP: ", p[1])
    p[0] = p[1]

def p_AND_OP(p):
    '''AND_OP : lpr and EXP AND_EXP_PLUS rpr'''
    # print("AND_OP: ", p[3] and p[4])
    p[0] = p[3] and p[4]

def p_AND_EXP_PLUS(p):
    '''AND_EXP_PLUS : EXP
                    | EXP AND_EXP_PLUS'''
    # print("AND_EXP_PLUS: ", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] and p[2]

def p_OR_OP(p):
    '''OR_OP : lpr or EXP OR_EXP_PLUS rpr'''
    # print("OR_OP: ", p[3] or p[4])
    p[0] = p[3] or p[4]

def p_OR_EXP_PLUS(p):
    '''OR_EXP_PLUS  : EXP
                    | EXP OR_EXP_PLUS'''
    # print("OR_EXP_PLUS: ", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] or p[2]

def p_NOT_OP(p):
    '''NOT_OP : lpr not EXP rpr'''
    # print("NOT_OP: ", not p[3])
    p[0] = not p[3]

def p_DEF_STMT(p):
    '''DEF_STMT : lpr define VARIABLE EXP rpr'''
    # print("DEF_STMT: ", p[3], p[4])
    define_var[p[3]] = p[4]

def p_VARIABLE(p):
    '''VARIABLE : id'''
    # print("VARIABLE: ", p[1])
    p[0] = define_var[p[1]]

def p_FUN_EXP(p):
    '''FUN_EXP : lpr fun_ FUN_IDs FUN_BODY rpr'''
    # print("FUN_EXP: ", p[1])
def p_FUN_IDs(p):
    '''FUN_IDs  : lpr rpr
                | lpr ID_PLUS rpr'''
    # print("FUN_IDs: ", p[1])
def p_ID_PLUS(p):
    '''ID_PLUS  : id
                | id ID_PLUS'''
    # print("ID_PLUS: ", p[1])
def p_FUN_BODY(p):
    '''FUN_BODY  : EXP'''
    # print("FUN_BODY: ", p[1])
def p_FUN_CALL(p):
    '''FUN_CALL : lpr FUN_EXP rpr
                | lpr FUN_EXP PARAM_PLUS rpr
                | lpr FUN_NAME rpr
                | lpr FUN_NAME PARAM_PLUS rpr'''
    # print("p_FUN_CALL: ", p[1])
def p_PARAM(p):
    '''PARAM : EXP'''
    # print("p_PARAM: ", p[1])
def p_PARAM_PLUS(p):
    '''PARAM_PLUS   : PARAM
                    | PARAM PARAM_PLUS'''
    # print("p_PARAM_PLUS: ", p[1])
def p_FUN_NAME(p):
    '''FUN_NAME  : id'''
    # print("FUN_NAME: ", p[1])

def p_IF_EXP(p):
    '''IF_EXP : lpr if_ TEST_EXP THEN_EXP ELSE_EXP rpr'''
    # print("IF_EXP: ", p[3], p[4], p[5])
    if p[3]:
        p[0] = p[4]
    else:
        p[0] = p[5]

def p_TEST_EXP(p):
    '''TEST_EXP : EXP'''
    # print("TEST_EXP: ", p[1])
    p[0] = p[1]

def p_THEN_EXP(p):
    '''THEN_EXP : EXP'''
    # print("THEN_EXP: ", p[1])
    p[0] = p[1]

def p_ELSE_EXP(p):
    '''ELSE_EXP : EXP'''
    # print("ELSE_EXP: ", p[1])
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input: ", p)
    # print("syntax error")

# Build the parser
import sys
parser = yacc.yacc()

with open(sys.argv[1]) as f:
    s = f.read()
# lexer = lex.lexer
# lexer.input(s)
result = parser.parse(s)

# while True:
#     try:
#         # s = input()
#         with open(sys.argv[1]) as f:
#             s = f.read()
#         # s = sys.stdin.readline()
#     except EOFError:
#         break
#     if not s: continue
#     lexer = lex.lexer
#     lexer.input(s)
#     # while True:
#     #     tok = lexer.token()
#     #     if not tok: 
#     #         break      # No more input
#     #     print(tok)
#     result = parser.parse(s)
# #    print(result)