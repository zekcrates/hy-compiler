from __future__ import annotations
from compiler.types import Int, Bool, Unit, IntType, BoolType, UnitType, FunctionType
import compiler.ast as ast
from compiler.type_checking import typecheck, new_table 
Type = IntType | BoolType | UnitType | FunctionType

def tc(node: ast.Expression) -> Type:
    return typecheck(node, new_table())

def int_lit(n: int) -> ast.Literal:
    return ast.Literal(value=n)

def bool_lit(b: bool) -> ast.Literal:
    return ast.Literal(value=b)

def binop(left: ast.Expression, op: str, right: ast.Expression) -> ast.BinaryOp:
    return ast.BinaryOp(left=left, op=op, right=right)

def ident(name: str) -> ast.Identifier:
    return ast.Identifier(name=name)
