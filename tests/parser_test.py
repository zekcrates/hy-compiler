import compiler.ast as ast 
from compiler.tokenizer import Token, tokenize 
from compiler.parser import parse

def test_parser_test1()-> None :
    tokens = tokenize("1 + 2")
    parse_output =parse(tokens) 
    print("parse_output : " , parse_output)
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



def test_parser_func() -> None:
    tokens = tokenize("add(a,b)")
    parse_output = parse(tokens)
    print("\n\nparse_output : \n" , parse_output) 
    assert parse_output ==ast.Function(name='add', args=[ast.Identifier(name='a'), ast.Identifier(name='b')])


def test_parser_t4() -> None:
    tokens = tokenize("x = if a == 5 then add(x, 1 + 2) else y * -3")
    parse_output = parse(tokens)
    assert parse_output == ast.Assignment(target=ast.Identifier(name='x'), value=ast.IfExpr(condition=ast.BinaryOp(left=ast.Identifier(name='a'), op='==', right=ast.Literal(value=5)), then_branch=ast.Function(name='add', args=[ast.Identifier(name='x'), ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.Literal(value=2))]), else_branch=ast.BinaryOp(left=ast.Identifier(name='y'), op='*', right=ast.UnaryOp(op='-', expr=ast.Literal(value=3)))))



def test_parser_unary_not() -> None:
    tokens = tokenize("not x")
    parse_output = parse(tokens)
    assert parse_output == ast.UnaryOp(op='not', expr=ast.Identifier(name='x'))

def test_parser_chained_comparison() -> None:
    tokens = tokenize("x == y")
    parse_output = parse(tokens)
    assert parse_output == ast.BinaryOp(left=ast.Identifier(name='x'), op='==', right=ast.Identifier(name='y'))

def test_parser_and_or() -> None:
    tokens = tokenize("x and y or z")
    parse_output = parse(tokens)
    # or is lower precedence so it's the root
    assert parse_output == ast.BinaryOp(
        left=ast.BinaryOp(left=ast.Identifier(name='x'), op='and', right=ast.Identifier(name='y')),
        op='or',
        right=ast.Identifier(name='z')
    )

def parser_parenthesized() -> None:
    tokens = tokenize("(1 + 2) * 3")
    parse_output = parse(tokens)
    assert parse_output == ast.BinaryOp(
        left=ast.BinaryOp(left=ast.Literal(value=1), op='+', right=ast.Literal(value=2)),
        op='*',
        right=ast.Literal(value=3)
    )

def test_parser_chained_assignment() -> None:
    tokens = tokenize("x = y = 5")
    parse_output = parse(tokens)
    # right associative so y=5 happens first
    assert parse_output == ast.Assignment(
        target=ast.Identifier(name='x'),
        value=ast.Assignment(
            target=ast.Identifier(name='y'),
            value=ast.Literal(value=5)
        )
    )

def test_parser_nested_function() -> None:
    tokens = tokenize("add(f(x), y)")
    parse_output = parse(tokens)
    assert parse_output == ast.Function(
        name='add',
        args=[
            ast.Function(name='f', args=[ast.Identifier(name='x')]),
            ast.Identifier(name='y')
        ]
    )

def test_parser_if_else_complex() -> None:
    tokens = tokenize("if x and y then 1 else 0")
    parse_output = parse(tokens)
    assert parse_output == ast.IfExpr(
        condition=ast.BinaryOp(left=ast.Identifier(name='x'), op='and', right=ast.Identifier(name='y')),
        then_branch=ast.Literal(value=1),
        else_branch=ast.Literal(value=0)
    )

# error cases
def test_parser_empty_parens_error() -> None:
    tokens = tokenize("()")
    try:
        parse(tokens)
        assert False
    except Exception:
        assert True

def test_parser_missing_then_error() -> None:
    tokens = tokenize("if x 5")
    try:
        parse(tokens)
        assert False
    except Exception:
        assert True

def test_block_basic() -> None:
    tokens = tokenize("{ a; b }")
    parse_output = parse(tokens)
    assert parse_output == ast.Block(statements=[
        ast.Identifier(name='a'),
        ast.Identifier(name='b')
    ])

def test_block_trailing_semicolon() -> None:
    tokens = tokenize("{ a; b; }")
    parse_output = parse(tokens)
    assert parse_output == ast.Block(statements=[
        ast.Identifier(name='a'),
        ast.Identifier(name='b'),
        ast.Literal(value=None)
    ])

def test_block_missing_semicolon_error() -> None:
    tokens = tokenize("{ a b }")
    try:
        parse(tokens)
        assert False
    except Exception:
        assert True


def test_var_1() -> None:
    tokens = tokenize("var x = 3 ") 
    parse_output = parse(tokens) 
    assert parse_output ==ast.VarDecl(name='x', var_type=None, value=ast.Literal(value=3))

