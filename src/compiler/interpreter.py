from typing import Any 
from compiler import ast 

Value = int | bool | None 


def interpret(node: ast.Expression) -> Value:
    match node: 
        case ast.Literal() :
            return  node.value 
        
        case ast.BinaryOp():
            a:Any =  interpret(node.left) 
            b: Any = interpret(node.right) 
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
                return interpret(node.then_branch) 
            else:
                return interpret(node.else_branch)
        
        case ast.UnaryOp():
            c: Any = interpret(node.expr) 
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
                val = interpret(expr) 
                arg_vals.append(val) 

            if node.name == "print":
                print(*arg_vals)
                raise Exception("n")
            else:
                raise Exception("Unknown error at Function" ) 


        case _:
            raise Exception(f"Unsupported node type: {type(node).__name__}")

    return None
