import compiler.ast as ast 
from compiler.tokenizer import Token, tokenize 
from compiler.parser import parse

def test_parser_test1()-> None :
    tokens = tokenize("1 + 2")
    parse_output =parse(tokens) 

    assert parse_output == ast.BinaryOp(left=ast.Literal(value=1) , op='+', right=ast.Literal(value=2))


def test_parser_test2() -> None:
    tokens = tokenize("1+2 * 3")
    parse_output = parse(tokens) 

    assert parse_output ==ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.BinaryOp(left=ast.Literal(value=2), op='*', right=ast.Literal(value=3)))


#make sure (a+b c) give error 
def test_parser_test3() -> None:
    tokens = tokenize("a + b c ") 
    try: 
        parse_output = parse(tokens) 
        assert False 
    except Exception:
        assert True 


def test_parser_ifthen() ->None :
    tokens = tokenize("if a + b then b+c ") 
    
    parse_output = parse(tokens) 
    assert parse_output == ast.IfExpr(condition=ast.BinaryOp(left=ast.Identifier(name='a'), op='+', right=ast.Identifier(name='b')), then_branch=ast.BinaryOp(left=ast.Identifier(name='b'), op='+', right=ast.Identifier(name='c')), else_branch=None)



def test_parser_ifthen2() -> None:
    tokens =tokenize("if x then if y + 2 then z")
    parse_output = parse(tokens) 

    assert parse_output == ast.IfExpr(condition=ast.Identifier(name='x'), then_branch=ast.IfExpr(condition=ast.BinaryOp(left=ast.Identifier(name='y'), op='+', right=ast.Literal(value=2)), then_branch=ast.Identifier(name='z'), else_branch=None), else_branch=None)

