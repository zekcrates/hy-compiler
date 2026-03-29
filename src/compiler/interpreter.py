from typing import Any 
from compiler import ast 

Value = int | bool | None 

class SymTab:
    def __init__(self, parent=None):
        self.locals: dict[str, Value] = {}  
        self.parent: SymTab | None = parent

def interpret(node: ast.Expression, symtab=None) -> Value:
    match node: 
        case ast.Literal() :
            return  node.value 
        
        case ast.BinaryOp():
            a:Any =  interpret(node.left, symtab) 
            b: Any = interpret(node.right), symtab )  
            if node.op == '+':
                return a + b 
            elif node.op == '<':
                return a< b 
            elif node.op == '-':
                return a-b 
            
            else :
                raise Exception("Unknown error at binaryop" ) 

        case ast.IfThen():
            if (interpret(node.condition)):
                return interpret(node.then_branch, symtab) 
            else:
                return interpret(node.else_branch, symtab)
        
        case ast.UnaryOp():

            c: Any = interpret(node.expr, symtab) 
            if node.op == '-':
                return -c
            elif node.op == 'not':
                return not c 
            else:
                raise Exception("Unknown error at unaryop") 

        case ast.Function():
           arg_vals = []
           if node.args is not None:

            for expr in node.args:
                val = interpret(expr, symtab) 
                arg_vals.append(val) 

            if node.name == "print":
                print(*arg_vals)
                return None 
            else:
                raise Exception("Unknown error at Function" ) 

        case ast.VarDecl():
            name = node.name 
            value = interpret(node.value, symtab) 
            SymTab.locals[name] = value 
            return value 

        case ast.Block():
            result = None 
            block_table = SymTab(parent=symtab) 
            for st in node.statements:
                result = interpret(st, block_table) 
            return result 
        case _:
            raise Exception(f"Unsupported node type: {type(node).__name__}")

    return None
