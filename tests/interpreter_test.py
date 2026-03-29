import compiler.ast as  ast 
from compiler.tokenizer import tokenize , Token 
from compiler.interpreter import interpret
from compiler.parser import parse

def test_interpreter_basic() -> None :
    tokens =tokenize("3 + 2 " ) 
    parse_output = parse(tokens ) 
    output = interpret(parse_output) 

    print(output)
    assert output == 5 
