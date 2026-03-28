from dataclasses import dataclass 
from compiler.tokenizer import SourceLocation
@dataclass 
class Expression:
     """Base class for AST nodes representing expressions."""

@dataclass
class Literal(Expression):
    value: int| bool | None 
    # a = Literal(1) or Literal(True) 

    location : SourceLocation | None = None 

@dataclass 
class Identifier(Expression):
    name: str 
    #a = Identifier("x") 

    location : SourceLocation | None = None 
@dataclass 
class BinaryOp(Expression):
    left: Expression 
    op: str 
    right: Expression 
    
    location : SourceLocation | None = None 

@dataclass
class IfExpr(Expression):
    condition : Expression 
    then_branch: Expression     
    else_branch : Expression | None = None 
    
    location : SourceLocation | None = None 

@dataclass 
class Function(Expression):
    name: str 
    args: list[Expression] | None = None 

    location : SourceLocation | None = None 

@dataclass
class UnaryOp(Expression):
    op: str 
    expr: Expression 
    
    location : SourceLocation | None = None 

@dataclass 
class Assignment(Expression):
    target: Expression 
    value: Expression 

    location : SourceLocation | None = None 
@dataclass
class Block(Expression):
    statements: list[Expression] 

    location : SourceLocation | None = None 

@dataclass
class VarDecl(Expression):
    name: str 
    var_type: str | None = None 
    value : Expression | None = None 

    location : SourceLocation | None = None 
