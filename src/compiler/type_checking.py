from __future__ import annotations
import compiler.ast as ast
from compiler.types import Int, Bool, Unit, FunctionType, IntType, BoolType, UnitType
from typing import Optional

Type = IntType | BoolType | UnitType | FunctionType


class SymTab:
    def __init__(self, parent: Optional[SymTab] = None) -> None:
        self.locals: dict[str, Type] = {}
        self.parent: Optional[SymTab] = parent

def new_table() -> SymTab:
        top = SymTab()
        top.locals['+'] = FunctionType([Int,Int],Int)
        top.locals['-'] = FunctionType([Int,Int], Int) 
        top.locals['*'] = FunctionType([Int,Int], Int) 
        top.locals['/'] = FunctionType([Int,Int], Int) 
        top.locals['<'] = FunctionType([Int,Int], Bool) 
        top.locals['>'] = FunctionType([Int,Int], Bool) 
        top.locals['<='] = FunctionType([Int,Int], Bool)
        top.locals['>='] = FunctionType([Int,Int], Bool ) 
        top.locals['unary_not'] = FunctionType([Bool], Bool)
        top.locals['unary_-']   = FunctionType([Int], Int)
        top.locals['print_int'] = FunctionType([Int], Unit)
        top.locals['print_bool']= FunctionType([Bool], Unit)
        return top 
def typecheck(node: ast.Expression, symtab: SymTab) -> Type:
    match node: 
        case ast.BinaryOp():
            t1 = typecheck(node.left, symtab)
            t2 = typecheck(node.right, symtab) 
            if node.op in ('==', '!='):
                if t1 != t2:
                    raise Exception(f"== / != requires same type on both sides")
                return Bool 
            op_type = lookup(node.op, symtab)
            if not isinstance(op_type, FunctionType):
                raise Exception(f"{node.op} is not a function type")
            if [t1, t2] != op_type.param_types:
                raise Exception(f"Wrong types for operator {node.op}")
            return op_type.return_type


        case ast.UnaryOp():
            t = typecheck(node.expr, symtab) 
            op_type = lookup('unary_' + node.op, symtab) 
            if not isinstance(op_type, FunctionType) :
                raise Exception("Type is not functiontype") 

            if [t] != op_type.param_types:
                raise Exception("Types dont match") 
            return op_type.return_type

        case ast.IfExpr():
            cond = typecheck(node.condition, symtab) 
            if cond is not Bool:
                raise Exception("Wrong type for bool") 
            then = typecheck(node.then_branch, symtab) 
            else_b = None
            if node.else_branch is not None:

                else_b = typecheck(node.else_branch, symtab) 
            if else_b is not None and then != else_b:
                raise Exception("Wrong type condition") 
            return then 
        
        case ast.Literal():
            if isinstance(node.value , bool) :
                return Bool 
            elif isinstance(node.value, int) :
                return Int
            else:
                raise Exception("Type other than int/bool") 


        case ast.VarDecl():
            name = node.name 
            val = typecheck(node.value, symtab) 
            if node.var_type is not None and  node.var_type != val :
                raise Exception("Types dont match") 

            symtab.locals[name] = val 
            return val 

        case ast.Function():
            func_type = lookup(node.name , symtab) 
            if not isinstance(func_type, FunctionType):                                     raise Exception(f"{node.name} is not a function") 
            
            args = node.args or []
            arg_types = [typecheck(x, symtab) for x in args]

            if len(arg_types) != len(func_type.param_types):
                raise Exception(f"Wrong number of arguments for {node.name}")
        
            for i, (got, expected) in enumerate(zip(arg_types, func_type.param_types)):
                if got != expected:
                    raise Exception(
                        f"Argument {i+1} of {node.name}: expected {expected}, got {got}"
            )
            return func_type.return_type
        case ast.Identifier():
            return lookup(node.name , symtab) 
    
        case ast.Block():
            result:Type = Unit 
            child = SymTab(parent=symtab) 
            for ex in node.statements:
                result = typecheck(ex, child) 
            return result 
        case _:
            raise Exception("Unsupported node type")        


def lookup(name: str, symtab: SymTab) -> Type: 
    if name in symtab.locals:
        return symtab.locals[name] 
    elif symtab.parent  is not None:
        return lookup(name ,symtab.parent ) 
    else:
        raise Exception(f"Undefined type for variable {name}") 
