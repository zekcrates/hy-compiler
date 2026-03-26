from compiler.tokenizer import Token 
from compiler.ast import ast 


def parse(tokens: list[Token]) -> ast.Expression :
    pos = 0 

    def peek()-> Token:
        # return token at pos 
        if pos < len(tokens) :
            return tokens[pos] 
        else:
            return Token(text="", type="end" , loc=tokens[-1].loc) 
    

    def consume(expected: str | list[str] | None) -> Token: 
        nonlocal pos 
        token = peek() 
        if isinstance(expected,str) and token.text != expected: 
            raise Exception(f'{token.loc}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected: 
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f'{token.loc}: expected one of: {comma_separated}')

        pos +=1 
        return token 

    
    def parse_int_literal() -> ast.Literal:
        if peek().type != "int_literal":
            raise Exception(f'{peek().location}: expected an integer literal')
        token = consume() 
        return ast.Literal(int(token.text)) 

    def parse_expression() -> ast.BinaryOp:
        left = parse_int_literal()
        operator_token = consume(['+', '-']) 
        right = parse_int_literal() 
        return ast.BinaryOp(left,operator_token.text , right )

    return parse_expression() 



a = Token(text="1" , type="int_literal")
b  = Token(text="2", type="int_literal") 
tokens =[a,b] 
print(parse(tokens) ) 

