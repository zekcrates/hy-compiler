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
        case _:
            raise Exception(f"Unsupported node type: {type(node).__name__}")
