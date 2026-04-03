from __future__ import annotations
from typing import Any,Callable
from compiler import ast 
from typing import Optional  , Any, cast
Value = int | bool | None | Callable[..., Any]


class SymTab:
    def __init__(self, parent:Optional[SymTab]=None):
        self.locals: dict[str, Value] = {}  
        self.parent: Optional[SymTab] = parent

def new_table()-> SymTab:
    top = SymTab()
    top.locals['+'] = lambda a, b: a + b
    top.locals['-'] = lambda a, b: a - b
    top.locals['*'] = lambda a, b: a * b
    top.locals['/'] = lambda a, b: a // b
    top.locals['<'] = lambda a, b: a < b
    top.locals['>'] = lambda a, b: a > b
    top.locals['<='] = lambda a, b : a<= b 
    top.locals['>='] =lambda a,b : a>= b 
    top.locals['=='] = lambda a, b: a == b
    top.locals['!='] = lambda a, b: a != b
    top.locals['unary_not'] = lambda a: not a
    top.locals['unary_-'] = lambda a: -a
    top.locals['print_int'] = lambda a: print(a)
    top.locals['print_bool'] = lambda a: print(a) 
    return top 

def interpret(node: ast.Expression, symtab:SymTab| None=None) -> Value:
    if symtab is None:
        symtab = new_table()
    match node: 
        case ast.Literal() :
            return  node.value 
        
        case ast.BinaryOp():
            if node.op == '=':
                value = interpret(node.right, symtab)
                if not isinstance(node.left, ast.Identifier):
                    raise Exception("Assignment target must be an identifier")
                symtab.locals[node.left.name] = value 

                return value
            elif node.op == "and":
                return interpret(node.left, symtab) and interpret(node.right , symtab) 


            elif node.op == "or":
                    # dont check the right 

                return interpret(node.left, symtab) or interpret(node.right, symtab) 
            else:

                a:Any =  interpret(node.left, symtab) 
                b: Any = interpret(node.right, symtab )  
                func = lookup(node.op , symtab)
                if not callable(func):
                     raise Exception(f"{node.op} is not callable")
                return cast(Callable[..., Any], func)(a, b)
 

        case ast.IfThen():
            if (interpret(node.condition)):
                return interpret(node.then_branch, symtab) 
            else:
                return interpret(node.else_branch, symtab)
        
        case ast.UnaryOp():

            c: Any = interpret(node.expr, symtab) 
            func = lookup('unary_' + node.op, symtab)
            if not callable(func):
                raise Exception(f"unary_{node.op} is not callable")
            return cast(Callable[..., Any], func)(c)
             

        case ast.Function():
           arg_vals = []
           if node.args is not None:

            for expr in node.args:
                val = interpret(expr, symtab) 
                arg_vals.append(val) 

            func = lookup(node.name, symtab)
            if not callable(func):
                raise Exception(f"{node.name} is not callable")
            return cast(Callable[..., Any], func)(*arg_vals)

        case ast.VarDecl():
            name = node.name 
            value = interpret(node.value, symtab) 
            symtab.locals[name] = value 
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
