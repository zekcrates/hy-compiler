from typing import Any,Callable 
from compiler import ast 

Value = int | bool | None | Callable 


class SymTab:
    def __init__(self, parent=None):
        self.locals: dict[str, Value] = {}  
        self.parent: SymTab | None = parent

def new_table()-> SymTab:
    top = SymTab()
    top.locals("+") = lambda a,b : a+b 
    top.locals("-") = lambda a,b: a-b 
    top.locals("<") = lambda a, b: a< b 
    top.locals("print_int") = lambda a: print(a) 
    
    return top 

def interpret(node: ast.Expression, symtab=None) -> Value:
    match node: 
        case ast.Literal() :
            return  node.value 
        
        case ast.BinaryOp():
            a:Any =  interpret(node.left, symtab) 
            b: Any = interpret(node.right), symtab )  
            func = lookup(node.op , symtab) 
            return func(a,b) 

        case ast.IfThen():
            if (interpret(node.condition)):
                return interpret(node.then_branch, symtab) 
            else:
                return interpret(node.else_branch, symtab)
        
        case ast.UnaryOp():

            c: Any = interpret(node.expr, symtab) 
            func = lookup(node.name, symtab) 
            return func(c) 

        case ast.Function():
           arg_vals = []
           if node.args is not None:

            for expr in node.args:
                val = interpret(expr, symtab) 
                arg_vals.append(val) 

            func = lookup(node.name, symtab)
            return func(*arg_vals) 

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
        case ast.Identifier():
            return lookup(node.name, symtab) 

        case _:
            raise Exception(f"Unsupported node type: {type(node).__name__}")

    return None

def lookup(name: str, symtab: SymTab) -> Value:
    
    if name in symtab.locals:
        return symtab.locals[name] 
    elif symtab.parent is not None:
        return lookup(name, symtab.parent)
    else:
        raise Exception(f"Undefined variable {name} " ) 
