from __future__ import annotations
from compiler.types import Int, Bool, Unit, IntType, BoolType, UnitType, FunctionType
import compiler.ast as ast
from compiler.type_checking import typecheck, new_table 
Type = IntType | BoolType | UnitType | FunctionType
import pytest
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


def test_int_literal()-> None:
    assert tc(int_lit(10)) is Int 


def test_bool_literal_t()-> None:
    assert tc(bool_lit(True)) is Bool
    assert tc(bool_lit(False)) is Bool 

def test_add_ints() -> None:
    assert tc(binop(int_lit(1), '+', int_lit(2))) is Int
    assert tc(binop(int_lit(5), '-', int_lit(3))) is Int
    assert tc(binop(int_lit(2), '*', int_lit(4))) is Int
    assert tc(binop(int_lit(8), '/', int_lit(2))) is Int
    
    with pytest.raises(Exception):
        tc(binop(bool_lit(True), '+', int_lit(1)))

    with pytest.raises(Exception):
        tc(binop(bool_lit(True), '+', bool_lit(False)))

def test_lge()-> None:
    assert tc(binop(int_lit(3) , '<' , int_lit(5))) is Bool
    assert tc(binop(int_lit(3), '>', int_lit(1))) is Bool
    assert tc(binop(int_lit(1), '<=', int_lit(1))) is Bool
    assert tc(binop(int_lit(2), '>=', int_lit(2))) is Bool
    with pytest.raises(Exception):
        tc(binop(bool_lit(True), '<', int_lit(1)))

    assert tc(binop(int_lit(1), '==', int_lit(1))) is Bool
    assert tc(binop(bool_lit(True), '==', bool_lit(False))) is Bool
    assert tc(binop(int_lit(1), '!=', int_lit(2))) is Bool


def test_unary() -> None:
    assert tc(ast.UnaryOp(op='-', expr=int_lit(5))) is Int
    assert tc(ast.UnaryOp(op='not', expr=bool_lit(True))) is Bool

def test_var_decl()-> None:
    symtab = new_table()
    n = ast.VarDecl(name='flag', var_type=None, value=bool_lit(True))
    node = ast.VarDecl(name='x', var_type=None, value=int_lit(10))
    typecheck(node, symtab) 
    assert symtab.locals['x'] is Int 
    typecheck(n, symtab) 
    assert symtab.locals['flag'] is Bool 


def test_identifier_lookup() -> None:
    symtab = new_table()
    symtab.locals['x'] = Int
    assert typecheck(ident('x'), symtab) is Int


def test_if_then() -> None:
    node = ast.IfExpr(
        condition=bool_lit(True),
        then_branch=int_lit(1),
        else_branch=int_lit(2)
    )
    assert tc(node) is Int

    n = ast.IfExpr(
        condition=bool_lit(True),
        then_branch=bool_lit(True),
        else_branch=bool_lit(False)
    )

    assert tc(n) is Bool 
        
    node = ast.IfExpr(
        condition=bool_lit(True),
        then_branch=int_lit(1),
        else_branch=None
    )

    result = tc(node)
    assert result is not None


def test_print_int()-> None:
    node = ast.Function(name='print_int', args=[int_lit(42)])
    assert tc(node) is Unit

    node = ast.Function(name='print_bool', args=[bool_lit(True)])
    assert tc(node) is Unit

