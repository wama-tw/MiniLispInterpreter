import ply.yacc as yacc
# Get the token map from the lexer. This is required.
from lex import tokens # lex -> filename
from anytree import NodeMixin, RenderTree

class Tree(object):
    def __init__(self, root, definer=None):
        self.root = root
        self.def_var = {}
        self.fun_trees = {}
        self.definer = definer

class AstNodeClass(NodeMixin):  # Add Node feature
    def __init__(self, type, value=None, parent=None, children=None):
        self.type = type
        if value != None:
            self.value = value
        self.parent = parent
        if children:
            self.children = children

main_tree = Tree(AstNodeClass('root'))

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

def p_STMT_PLUS_one(p):
    '''STMT_PLUS    : STMT'''
    p[1].parent = main_tree.root
def p_STMT_PLUS_more(p):
    '''STMT_PLUS    : STMT STMT_PLUS'''
    p[1].parent = main_tree.root

def p_STMT_exp(p):
    '''STMT : EXP'''
    p[0] = AstNodeClass("stmt")
    p[1].parent = p[0]
def p_STMT_def(p):
    '''STMT : DEF_STMT'''
    p[0] = p[1]
def p_STMT_print(p):
    '''STMT : PRINT_STMT'''
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

def p_EXP_bool(p):
    '''EXP : bool_'''
    p[0] = AstNodeClass("bool", value=p[1])
def p_EXP_number(p):
    '''EXP : number'''
    p[0] = AstNodeClass("number", value=p[1])
def p_EXP_var(p):
    '''EXP : VARIABLE'''
    p[0] = AstNodeClass("variable", value=p[1])
def p_EXP_num_op(p):
    '''EXP : NUM_OP'''
    p[0] = p[1]
def p_EXP_logical_op(p):
    '''EXP : LOGICAL_OP'''
    p[0] = p[1]
def p_EXP_fun_exp(p):
    '''EXP : FUN_EXP'''
    p[0] = p[1]
def p_EXP_fun_call(p):
    '''EXP : FUN_CALL'''
    p[0] = p[1]
def p_EXP_if(p):
    '''EXP : IF_EXP'''
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
    p[0] = p[1]

def p_PLUS(p):
    '''PLUS : lpr plus EXP PLUS_EXP_PLUS rpr'''
    p[0] = AstNodeClass("+")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_PLUS_EXP_PLUS_one(p):
    '''PLUS_EXP_PLUS : EXP'''
    p[0] = p[1]
def p_PLUS_EXP_PLUS_more(p):
    '''PLUS_EXP_PLUS : EXP PLUS_EXP_PLUS'''
    p[0] = AstNodeClass("+")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_MINUS(p):
    '''MINUS : lpr minus EXP EXP rpr'''
    p[0] = AstNodeClass("-")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_MULTIPLY(p):
    '''MULTIPLY : lpr mul EXP MUL_EXP_PLUS rpr'''
    p[0] = AstNodeClass("*")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_MUL_EXP_PLUS_one(p):
    '''MUL_EXP_PLUS : EXP'''
    p[0] = p[1]
def p_MUL_EXP_PLUS_more(p):
    '''MUL_EXP_PLUS : EXP MUL_EXP_PLUS'''
    p[0] = AstNodeClass("*")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_DIVIDE(p):
    '''DIVIDE : lpr div EXP EXP rpr'''
    p[0] = AstNodeClass("//")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_MODULUS(p):
    '''MODULUS : lpr mod EXP EXP rpr'''
    p[0] = AstNodeClass("%")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_GREATER(p):
    '''GREATER : lpr greater EXP EXP rpr'''
    p[0] = AstNodeClass(">")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_SMALLER(p):
    '''SMALLER : lpr smaller EXP EXP rpr'''
    p[0] = AstNodeClass("<")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_EQUAL(p):
    '''EQUAL : lpr equal EXP EQUAL_EXP_PLUS rpr'''
    p[0] = AstNodeClass("=")
    p[3].parent = p[0]
    if p[4].type == "=":
        for node in p[4].children:
            node.parent = p[0]
    else:
        p[4].parent = p[0]
def p_EQUAL_EXP_PLUS_one(p):
    '''EQUAL_EXP_PLUS   : EXP'''
    p[0] = p[1]
def p_EQUAL_EXP_PLUS_more(p):
    '''EQUAL_EXP_PLUS   : EXP EQUAL_EXP_PLUS'''
    p[0] = AstNodeClass("=")
    p[1].parent = p[0]
    if p[2].type == "=":
        for node in p[2].children:
            node.parent = p[0]
    else:
        p[2].parent = p[0]

def p_LOGICAL_OP(p):
    '''LOGICAL_OP : AND_OP
                  | OR_OP
                  | NOT_OP'''
    p[0] = p[1]

def p_AND_OP(p):
    '''AND_OP : lpr and EXP AND_EXP_PLUS rpr'''
    p[0] = AstNodeClass("and")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_AND_EXP_PLUS_one(p):
    '''AND_EXP_PLUS : EXP'''
    p[0] = p[1]
def p_AND_EXP_PLUS_more(p):
    '''AND_EXP_PLUS : EXP AND_EXP_PLUS'''
    p[0] = AstNodeClass("and")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_OR_OP(p):
    '''OR_OP : lpr or EXP OR_EXP_PLUS rpr'''
    p[0] = AstNodeClass("or")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_OR_EXP_PLUS_one(p):
    '''OR_EXP_PLUS  : EXP'''
    p[0] = p[1]
def p_OR_EXP_PLUS_more(p):
    '''OR_EXP_PLUS  : EXP OR_EXP_PLUS'''
    p[0] = AstNodeClass("or")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_NOT_OP(p):
    '''NOT_OP : lpr not EXP rpr'''
    p[0] = AstNodeClass("not")
    p[3].parent = p[0]

def p_DEF_STMT(p):
    '''DEF_STMT : lpr define VARIABLE EXP rpr'''
    name = AstNodeClass("define_name", value=p[3])
    p[0] = AstNodeClass("define")
    name.parent = p[0]
    p[4].parent = p[0]

def p_VARIABLE(p):
    '''VARIABLE : id'''
    p[0] = p[1]

def p_FUN_EXP(p):
    '''FUN_EXP : lpr fun_ FUN_IDs FUN_BODY rpr'''
    p[0] = AstNodeClass("fun")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_FUN_IDs_no_id(p):
    '''FUN_IDs  : lpr rpr'''
    p[0] = AstNodeClass("no_id")
def p_FUN_IDs_ids(p):
    '''FUN_IDs  : lpr ID_PLUS rpr'''
    p[0] = AstNodeClass("ids", value=p[2])

def p_ID_PLUS_one(p):
    '''ID_PLUS  : id'''
    p[0] = [p[1]]
def p_ID_PLUS_more(p):
    '''ID_PLUS  : id ID_PLUS'''
    p[0] = p[2] + [p[1]]

def p_FUN_BODY_no_def(p):
    '''FUN_BODY  : EXP'''
    p[0] = p[1]
def p_FUN_BODY_def_one(p):
    '''FUN_BODY  : DEF_STMT EXP'''
    p[0] = AstNodeClass("define_in_fun")
    p[2].parent = p[0]
    p[1].parent = p[0]
def p_FUN_BODY_def_two(p):
    '''FUN_BODY  : DEF_STMT DEF_STMT EXP'''
    p[0] = AstNodeClass("define_in_fun")
    p[3].parent = p[0]
    p[1].parent = p[0]
    p[2].parent = p[0]
def p_FUN_BODY_def_three(p):
    '''FUN_BODY  : DEF_STMT DEF_STMT DEF_STMT EXP'''
    p[0] = AstNodeClass("define_in_fun")
    p[4].parent = p[0]
    p[1].parent = p[0]
    p[2].parent = p[0]
    p[3].parent = p[0]
def p_FUN_BODY_def_four(p):
    '''FUN_BODY  : DEF_STMT DEF_STMT DEF_STMT DEF_STMT EXP'''
    p[0] = AstNodeClass("define_in_fun")
    p[4].parent = p[0]
    p[1].parent = p[0]
    p[2].parent = p[0]
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_FUN_CALL_exp_no_param(p):
    '''FUN_CALL : lpr FUN_EXP rpr'''
    p[0] = AstNodeClass("call_exp_no_param")
    p[2].parent = p[0]
def p_FUN_CALL_exp_params(p):
    '''FUN_CALL : lpr FUN_EXP PARAM_PLUS rpr'''
    p[0] = AstNodeClass("call_exp_params")
    p[2].parent = p[0]
    params = AstNodeClass("params")
    for param in p[3]:
        param.parent = params
    params.parent = p[0]
def p_FUN_CALL_name_no_param(p):
    '''FUN_CALL : lpr FUN_NAME rpr'''
    p[0] = AstNodeClass("call_name_no_param")
    p[2].parent = p[0]
def p_FUN_CALL_name_params(p):
    '''FUN_CALL : lpr FUN_NAME PARAM_PLUS rpr'''
    p[0] = AstNodeClass("call_name_params")
    p[2].parent = p[0]
    params = AstNodeClass("params")
    for param in p[3]:
        param.parent = params
    params.parent = p[0]

def p_PARAM(p):
    '''PARAM : EXP'''
    p[0] = p[1]
def p_PARAM_PLUS_one(p):
    '''PARAM_PLUS   : PARAM'''
    p[0] = [p[1]]
def p_PARAM_PLUS_more(p):
    '''PARAM_PLUS   : PARAM PARAM_PLUS'''
    p[0] = p[2] + [p[1]]

def p_FUN_NAME(p):
    '''FUN_NAME  : id'''
    p[0] = AstNodeClass("fun_name", value=p[1])

def p_IF_EXP(p):
    '''IF_EXP : lpr if_ TEST_EXP THEN_EXP ELSE_EXP rpr'''
    assign = AstNodeClass("assign")
    p[4].parent = assign
    p[5].parent = assign
    p[0] = AstNodeClass("if_branch")
    p[3].parent = p[0]
    assign.parent = p[0]

def p_TEST_EXP(p):
    '''TEST_EXP : EXP'''
    p[0] = p[1]

def p_THEN_EXP(p):
    '''THEN_EXP : EXP'''
    p[0] = p[1]

def p_ELSE_EXP(p):
    '''ELSE_EXP : EXP'''
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    # print("Syntax error in input: ", p)       # for debugging
    print("syntax error")
    sys.exit(1)

# Reversing a tuple using slicing technique
# New tuple is created
def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

# Build the parser
import sys, copy
parser = yacc.yacc()
with open(sys.argv[1]) as f:
    s = f.read()
# s = '''(define dist-square
#   (fun (x y)
#     (define square (fun (x) (* x x)))
#     (define hii (fun (x) (* x x)))
#     (define hi2 (fun () 0))
#     (+ (square x) (hii y) (hi2))
#   )
# )
# (print-num (dist-square 3 4))
# '''
debug = False
parser.parse(s)
main_tree.root.children = Reverse(main_tree.root.children)
if debug:
    print_tree(main_tree.root)
# print_tree(main_tree.root)                                # TODO: remove this

def calculate(node, runner=main_tree):
    if not hasattr(node, 'type'):
        print('Warning: ' + str(node) + ' is not a node')
        return node
    if debug:
        print('calculating: ')
        print_tree(node)
    if node.type == "print_num":
        print(int(calculate(node.children[0], runner)))
    if node.type == "print_bool":
        if calculate(node.children[0], runner) == True:
            print("#t")
        else:
            print("#f")
    if node.type == "number":
        if debug:
            print('returning: ' + str(node.value))
        return node.value
    if node.type == "bool":
        if debug:
            print('returning: ' + str(node.value))
        return node.value
    if node.type == "+":
        res = 0
        for node in node.children:
            value = calculate(node, runner)
            if type(value) is not int:
                print("Type error!")
                sys.exit()
            res += value
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "-":
        first = calculate(node.children[0], runner)
        second = calculate(node.children[1], runner)
        if (type(first) is not int) or (type(second) is not int):
            print("Type error!")
            sys.exit()
        res = first - second
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "*":
        res = 1
        for node in node.children:
            value = calculate(node, runner)
            if type(value) is not int:
                print("Type error!")
                sys.exit()
            res *= value
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "//":
        first = calculate(node.children[0], runner)
        second = calculate(node.children[1], runner)
        if (type(first) is not int) or (type(second) is not int):
            print("Type error!")
            sys.exit()
        res = first // second
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "%":
        first = calculate(node.children[0], runner)
        second = calculate(node.children[1], runner)
        if (type(first) is not int) or (type(second) is not int):
            print("Type error!")
            sys.exit()
        res = first % second
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == ">":
        first = calculate(node.children[0], runner)
        second = calculate(node.children[1], runner)
        if (type(first) is not int) or (type(second) is not int):
            print("Type error!")
            sys.exit()
        res = (first > second)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "<":
        first = calculate(node.children[0], runner)
        second = calculate(node.children[1], runner)
        if (type(first) is not int) or (type(second) is not int):
            print("Type error!")
            sys.exit()
        res = (first < second)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "=":
        res = True
        value = calculate(node.children[0], runner)
        for node in node.children:
            next_value = calculate(node, runner)
            if type(next_value) is not int:
                print("Type error!")
                sys.exit()
            res = (res and (next_value == value))
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "and":
        res = True
        for node in node.children:
            value = calculate(node, runner)
            if type(value) is not bool:
                print("Type error!")
                sys.exit()
            res = (value and res)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "or":
        res = False
        for node in node.children:
            value = calculate(node, runner)
            if type(value) is not bool:
                print("Type error!")
                sys.exit()
            res = (value or res)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "not":
        value = calculate(node.children[0], runner)
        if type(value) is not bool:
            print("Type error!")
            sys.exit()
        res = not value
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "if_branch":
        res = None
        test_value = calculate(node.children[0], runner)
        if type(test_value) is not bool:
            print('Type error!')
            sys.exit()
        if test_value:
            res = calculate(node.children[1].children[0], runner)
        else:
            res = calculate(node.children[1].children[1], runner)
        if debug:
            print('returning:'+ str(res))
        return res
    if node.type == "variable":
        if debug:
            print(runner.def_var)
            print(runner.fun_trees)
            print_tree(node)
        if node.value in runner.def_var:
            if debug:
                if hasattr(runner.def_var[node.value], 'type'):
                    print_tree(runner.def_var[node.value])
                else:
                    print(runner.def_var[node.value])
            return calculate(runner.def_var[node.value], runner)
        elif runner.definer != None:
            definer = runner.definer
            while definer != None:
                if node.value in definer.def_var:
                    if debug:
                        print_tree(definer.def_var[node.value])
                    return calculate(definer.def_var[node.value], definer)
                definer = definer.definer
        print('variable ' + str(node.value) + ' not defined')
        sys.exit()
    if node.type == 'call_exp_no_param':
        return calculate(node.children[0].children[1], runner)
    if node.type == 'call_exp_params':
        if debug:
            print('variables: ' + str(runner.def_var))
            print('functions: ' + str(runner.fun_trees))
            print('definer: ' + str(runner.definer))
        tmp_tree = Tree(node.children[0].children[1], runner)
        params_index = 0
        for id in node.children[0].children[0].value:
            tmp_tree.def_var[id] = node.children[1].children[params_index]
            if debug:
                print_tree(tmp_tree.def_var[id])
            params_index += 1
        if debug:
            print(tmp_tree.def_var)
        return calculate(tmp_tree.root, tmp_tree)
    if node.type == 'call_name_no_param':
        if debug:
            print('variables: ' + str(runner.def_var))
            print('functions: ' + str(runner.fun_trees))
            print('definer: ' + str(runner.definer))
        fun_name = node.children[0].value
        if fun_name in runner.fun_trees:
            fun_tree = runner.fun_trees[fun_name]
            if debug:
                print_tree(fun_tree.root)
            return calculate(fun_tree.root.children[1], fun_tree)
        elif runner.definer != None:
            definer = runner.definer
            while definer != None:
                if fun_name in definer.fun_trees:
                    fun_tree = definer.fun_trees[fun_name]
                    if debug:
                        print_tree(fun_tree.root)
                    return calculate(fun_tree.root.children[1], fun_tree)
                definer = definer.definer
        print('function ' + str(fun_name) + ' not defined')
        sys.exit()
    if node.type == 'call_name_params':
        if debug:
            print('variables: ' + str(runner.def_var))
            print('functions: ' + str(runner.fun_trees))
            print('definer: ' + str(runner.definer))
        fun_name = node.children[0].value
        if fun_name in runner.fun_trees:
            fun_tree = copy.deepcopy(runner.fun_trees[fun_name])
            params_index = 0
            for id in fun_tree.root.children[0].value:
                id_value = calculate(node.children[1].children[params_index], runner)
                if type(id_value) is int:
                    id_node = AstNodeClass("number", value=id_value)
                elif type(id_value) is bool:
                    id_node = AstNodeClass("bool", value=id_value)
                fun_tree.def_var[id] = id_node
                if debug:
                    print_tree(fun_tree.def_var[id])
                params_index += 1
            return calculate(fun_tree.root.children[1], fun_tree)
        elif runner.definer != None:
            definer = runner.definer
            while definer != None:
                if fun_name in definer.fun_trees:
                    fun_tree = copy.deepcopy(definer.fun_trees[fun_name])
                    params_index = 0
                    for id in fun_tree.root.children[0].value:
                        param_node = AstNodeClass("number", value=calculate(node.children[1].children[params_index], runner))
                        fun_tree.def_var[id] = param_node
                        if debug:
                            if hasattr(fun_tree.def_var[id], 'type'):
                                print_tree(fun_tree.def_var[id])
                            else:
                                print(fun_tree.def_var[id])
                        params_index += 1
                    return calculate(fun_tree.root.children[1], fun_tree)
                definer = definer.definer
        print('function ' + str(fun_name) + ' not defined')
        sys.exit()

def define_(node, definer=main_tree):
    if debug:
        print('defining: ')
        print_tree(node)
    if node.children[1].type != 'fun':  # define value
        if node.children[0].value in definer.def_var:
            print('Redefining is not allowed.')
            sys.exit(0)
        definer.def_var[node.children[0].value] = node.children[1]
    elif node.children[1].children[1].type != 'define_in_fun':                               # define function
        definer.fun_trees[node.children[0].value] = Tree(node.children[1], definer)
    else:
        new_fun_tree_root = AstNodeClass("fun")
        new_fun_ids = copy.deepcopy(node.children[1].children[0])
        new_fun_body = copy.deepcopy(node.children[1].children[1].children[0])
        new_fun_ids.parent = new_fun_tree_root
        new_fun_body.parent = new_fun_tree_root
        if debug:
            print_tree(new_fun_tree_root)
        new_fun_tree = definer.fun_trees[node.children[0].value] = Tree(new_fun_tree_root, definer)
        for i in range(1, len(node.children[1].children[1].children)):
            sub_fun_define = node.children[1].children[1].children[i]
            define_(sub_fun_define, new_fun_tree)

for line_node in main_tree.root.children:
    if line_node.type == "stmt":
        calculate(line_node.children[0])
    elif line_node.type == "define":
        define_(line_node)
