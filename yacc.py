import ply.yacc as yacc
# Get the token map from the lexer. This is required.
from lex import tokens # lex -> filename
from anytree import NodeMixin, RenderTree

class Tree(object):
    def __init__(self, root, caller=None):
        self.root = root
        self.def_var = {}
        if caller:
            self.caller = caller

class AstNodeClass(NodeMixin):  # Add Node feature
    def __init__(self, type, value=None, parent=None, children=None):
        self.type = type
        if value != None:
            self.value = value
        self.parent = parent
        if children:
            self.children = children

main_tree = Tree(AstNodeClass('root'))
fun_trees = []

def print_tree(tree):
    for pre, _, node in RenderTree(tree):
        tree_str = u"%s%s" % (pre, node.type)
        if hasattr(node, 'value'):
            print(tree_str.ljust(8), node.value)
        else:
            print(tree_str.ljust(8))
    print('\n')

def p_PROGRAM(p):
    'PROGRAM : STMT_PLUS'
    # print("program: ", p[1])

def p_STMT_PLUS_one(p):
    '''STMT_PLUS    : STMT'''
    # print("stmts: ", p[1])
    p[1].parent = main_tree.root
def p_STMT_PLUS_more(p):
    '''STMT_PLUS    : STMT STMT_PLUS'''
    # print("stmts: ", p[1])
    p[1].parent = main_tree.root

def p_STMT_exp(p):
    '''STMT : EXP'''
    # print("stmt: ", p[1])
    p[0] = AstNodeClass("stmt")
    p[1].parent = p[0]
def p_STMT_def(p):
    '''STMT : DEF_STMT'''
    # print("stmt: ", p[1])
    p[0] = p[1]
def p_STMT_print(p):
    '''STMT : PRINT_STMT'''
    # print("stmt: ", p[1])
    p[0] = AstNodeClass("stmt")
    p[1].parent = p[0]

def p_PRINT_STMT(p):
    '''PRINT_STMT : lpr print_num EXP rpr
                  | lpr print_bool EXP rpr'''
    if p[2] == 'print-num':
        p[0] = AstNodeClass("print_num")
        p[3].parent = p[0]
    elif p[2] == 'print-bool':
        p[0] = AstNodeClass("print_bool")
        p[3].parent = p[0]
        # print(bool(p[3]))

def p_EXP_bool(p):
    '''EXP : bool_'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = AstNodeClass("bool", value=p[1])
def p_EXP_number(p):
    '''EXP : number'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = AstNodeClass("number", value=p[1])
def p_EXP_var(p):
    '''EXP : VARIABLE'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = AstNodeClass("variable", value=p[1])
def p_EXP_num_op(p):
    '''EXP : NUM_OP'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = p[1]
def p_EXP_logical_op(p):
    '''EXP : LOGICAL_OP'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = p[1]
def p_EXP_fun_exp(p):
    '''EXP : FUN_EXP'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = p[1]
def p_EXP_fun_call(p):
    '''EXP : FUN_CALL'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = p[1]
def p_EXP_if(p):
    '''EXP : IF_EXP'''
    # print("exp: ", p[1], p.lexpos(1))
    p[0] = p[1]

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
    p[0] = AstNodeClass("+")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_PLUS_EXP_PLUS_one(p):
    '''PLUS_EXP_PLUS : EXP'''
    # print("plusexps: ", p[1])
    p[0] = p[1]
def p_PLUS_EXP_PLUS_more(p):
    '''PLUS_EXP_PLUS : EXP PLUS_EXP_PLUS'''
    # print("plusexps: ", p[1])
    p[0] = AstNodeClass("+")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_MINUS(p):
    '''MINUS : lpr minus EXP EXP rpr'''
    # print("minus: ", p[3] - p[4])
    p[0] = AstNodeClass("-")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_MULTIPLY(p):
    '''MULTIPLY : lpr mul EXP MUL_EXP_PLUS rpr'''
    # print("multiply: ", p[3] * p[4])
    p[0] = AstNodeClass("*")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_MUL_EXP_PLUS_one(p):
    '''MUL_EXP_PLUS : EXP'''
    # print("mul_exps: ", p[1])
    p[0] = p[1]
def p_MUL_EXP_PLUS_more(p):
    '''MUL_EXP_PLUS : EXP MUL_EXP_PLUS'''
    # print("mul_exps: ", p[1])
    p[0] = AstNodeClass("*")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_DIVIDE(p):
    '''DIVIDE : lpr div EXP EXP rpr'''
    # print("DIVIDE: ", p[3] // p[4])
    p[0] = AstNodeClass("//")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_MODULUS(p):
    '''MODULUS : lpr mod EXP EXP rpr'''
    # print("MODULUS: ", p[3] % p[4])
    p[0] = AstNodeClass("%")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_GREATER(p):
    '''GREATER : lpr greater EXP EXP rpr'''
    # print("GREATER: ", p[3] > p[4])
    p[0] = AstNodeClass(">")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_SMALLER(p):
    '''SMALLER : lpr smaller EXP EXP rpr'''
    # print("SMALLER: ", p[3] < p[4])
    p[0] = AstNodeClass("<")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_EQUAL(p):
    '''EQUAL : lpr equal EXP EQUAL_EXP_PLUS rpr'''
    # print("EQUAL: ", p[3] == p[4])
    p[0] = AstNodeClass("=")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_EQUAL_EXP_PLUS_one(p):
    '''EQUAL_EXP_PLUS   : EXP'''
    # print("EQUAL_EXP_PLUS: ", p[1])
    p[0] = p[1]
def p_EQUAL_EXP_PLUS_more(p):
    '''EQUAL_EXP_PLUS   : EXP EQUAL_EXP_PLUS'''
    # print("EQUAL_EXP_PLUS: ", p[1])
    p[0] = AstNodeClass("=")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_LOGICAL_OP(p):
    '''LOGICAL_OP : AND_OP
                  | OR_OP
                  | NOT_OP'''
    # print("LOGICAL_OP: ", p[1])
    p[0] = p[1]

def p_AND_OP(p):
    '''AND_OP : lpr and EXP AND_EXP_PLUS rpr'''
    # print("AND_OP: ", p[3] and p[4])
    p[0] = AstNodeClass("and")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_AND_EXP_PLUS_one(p):
    '''AND_EXP_PLUS : EXP'''
    # print("AND_EXP_PLUS: ", p[1])
    p[0] = p[1]
def p_AND_EXP_PLUS_more(p):
    '''AND_EXP_PLUS : EXP AND_EXP_PLUS'''
    # print("AND_EXP_PLUS: ", p[1])
    p[0] = AstNodeClass("and")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_OR_OP(p):
    '''OR_OP : lpr or EXP OR_EXP_PLUS rpr'''
    # print("OR_OP: ", p[3] or p[4])
    p[0] = AstNodeClass("or")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_OR_EXP_PLUS_one(p):
    '''OR_EXP_PLUS  : EXP'''
    # print("OR_EXP_PLUS: ", p[1])
    p[0] = p[1]
def p_OR_EXP_PLUS_more(p):
    '''OR_EXP_PLUS  : EXP OR_EXP_PLUS'''
    # print("OR_EXP_PLUS: ", p[1])
    p[0] = AstNodeClass("or")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_NOT_OP(p):
    '''NOT_OP : lpr not EXP rpr'''
    # print("NOT_OP: ", not p[3])
    p[0] = AstNodeClass("not")
    p[3].parent = p[0]

def p_DEF_STMT(p):
    '''DEF_STMT : lpr define VARIABLE EXP rpr'''
    # print("DEF_STMT: ", p[3], p[4])
    name = AstNodeClass("define_name", value=p[3])
    p[0] = AstNodeClass("define")
    name.parent = p[0]
    p[4].parent = p[0]

def p_VARIABLE(p):
    '''VARIABLE : id'''
    # print("VARIABLE: ", p[1])
    p[0] = p[1]

def p_FUN_EXP(p):
    '''FUN_EXP : lpr fun_ FUN_IDs FUN_BODY rpr'''
    # print("FUN_EXP: ", p[1])
    p[0] = AstNodeClass("fun")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_FUN_IDs_no_id(p):
    '''FUN_IDs  : lpr rpr'''
    # print("FUN_IDs: ", p[1])
    p[0] = AstNodeClass("no_id")
def p_FUN_IDs_ids(p):
    '''FUN_IDs  : lpr ID_PLUS rpr'''
    # print("FUN_IDs: ", p[1])
    p[0] = AstNodeClass("ids", value=p[2])

def p_ID_PLUS_one(p):
    '''ID_PLUS  : id'''
    # print("ID_PLUS: ", p[1])
    p[0] = [p[1]]
def p_ID_PLUS_more(p):
    '''ID_PLUS  : id ID_PLUS'''
    # print("ID_PLUS: ", p[1])
    p[0] = p[2] + [p[1]]

def p_FUN_BODY(p):
    '''FUN_BODY  : EXP'''
    # print("FUN_BODY: ", p[1])
    p[0] = p[1]

def p_FUN_CALL_exp_no_param(p):
    '''FUN_CALL : lpr FUN_EXP rpr'''
    # print("p_FUN_CALL: ", p[1])
    p[0] = AstNodeClass("call_exp_no_param")
    p[2].parent = p[0]
def p_FUN_CALL_exp_params(p):
    '''FUN_CALL : lpr FUN_EXP PARAM_PLUS rpr'''
    # print("p_FUN_CALL: ", p[1])
    p[0] = AstNodeClass("call_exp_params")
    p[2].parent = p[0]
    params = AstNodeClass("params")
    for param in p[3]:
        param.parent = params
    params.parent = p[0]
def p_FUN_CALL_name_no_param(p):
    '''FUN_CALL : lpr FUN_NAME rpr'''
    # print("p_FUN_CALL: ", p[1])
    p[0] = AstNodeClass("call_name_no_param")
    p[2].parent = p[0]
def p_FUN_CALL_name_params(p):
    '''FUN_CALL : lpr FUN_NAME PARAM_PLUS rpr'''
    # print("p_FUN_CALL: ", p[1])
    p[0] = AstNodeClass("call_name_params")
    p[2].parent = p[0]
    params = AstNodeClass("params")
    for param in p[3]:
        param.parent = params
    params.parent = p[0]

def p_PARAM(p):
    '''PARAM : EXP'''
    # print("p_PARAM: ", p[1])
    p[0] = p[1]
def p_PARAM_PLUS_one(p):
    '''PARAM_PLUS   : PARAM'''
    # print("p_PARAM_PLUS: ", p[1])
    p[0] = [p[1]]
def p_PARAM_PLUS_more(p):
    '''PARAM_PLUS   : PARAM PARAM_PLUS'''
    # print("p_PARAM_PLUS: ", p[1])
    p[0] = p[2] + [p[1]]

def p_FUN_NAME(p):
    '''FUN_NAME  : id'''
    # print("FUN_NAME: ", p[1])
    p[0] = AstNodeClass("fun_name", value=p[1])

def p_IF_EXP(p):
    '''IF_EXP : lpr if_ TEST_EXP THEN_EXP ELSE_EXP rpr'''
    # print("IF_EXP: ", p[3], p[4], p[5])
    assign = AstNodeClass("assign")
    p[4].parent = assign
    p[5].parent = assign
    p[0] = AstNodeClass("if_branch")
    p[3].parent = p[0]
    assign.parent = p[0]

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
    print("Syntax error in input: ", p)                           # TODO: change
    # print("syntax error")

# Build the parser
import sys
parser = yacc.yacc()

with open(sys.argv[1]) as f:
    s = f.read()
# lexer = lex.lexer
# lexer.input(s)
parser.parse(s)
print_tree(main_tree.root)












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