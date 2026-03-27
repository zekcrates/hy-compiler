from dataclasses import dataclass 

@dataclass 
class Expression:
     """Base class for AST nodes representing expressions."""


@dataclass
class Literal(Expression):
    value: int| bool 
    # a = Literal(1) or Literal(True) 


@dataclass 
class Identifier(Expression):
    name: str 
    #a = Identifier("x") 

@dataclass 
class BinaryOp(Expression):
    left: Expression 
    op: str 
    right: Expression 


@dataclass
class IfExpr(Expression):
    condition : Expression 
    then_branch: Expression     
    else_branch : Expression | None = None 


@dataclass 
class Function(Expression):
    name: str 
    args: list[Expression] | None = None 


@dataclass
class UnaryOp(Expression):
    op: str 
    expr: Expression 


@dataclass 
class Assignment(Expression):
    target: Expression 
    value: Expression 

