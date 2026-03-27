from compiler.tokenizer import Token 
import compiler.ast as ast 


def parse(tokens: list[Token]) -> ast.Expression :
    pos = 0 

    def peek()-> Token:
        # return token at pos
        if len(tokens) == 0 :
            raise SyntaxError("Unexpected end of input (no tokens to peek)")
        if pos < len(tokens) :
            return tokens[pos] 
        else:
            return Token(text="", type="end" , loc=tokens[-1].loc) 
    

    def consume(expected: str | list[str] | None=None) -> Token: 
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
            raise Exception(f'{peek().loc}: expected an integer literal')
        token = consume() 
        return ast.Literal(int(token.text)) 
    

    def parse_identifier() -> ast.Identifier:
        if peek().type != "identifier" :
            
            raise Exception(f'{peek().loc}: expected an identifier')
        token = consume() 
        return ast.Identifier(token.text)
    
    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().text == "if":
            return parse_if()
        elif peek().type == "int_literal" :
            return parse_int_literal() 
        elif peek().type == "identifier" :
            return parse_identifier() 
        else:
            raise Exception(f'{peek().loc}: expected an integer literal or an identifier')

    def parse_expression() -> ast.Expression:
        left = parse_term() 

        while peek().text in ['+', '-'] :
            operator_token = consume() 
            operator = operator_token.text 

            right = parse_term() 

            left = ast.BinaryOp(
                    left, 
                    operator, 
                    right
                    )            
        
        return left 
    

    def parse_term() -> ast.Expression:
        left = parse_factor() 

        while peek().text in ['*','/']:
            operator_token = consume() 
            operator = operator_token.text 
            right = parse_factor()
            left = ast.BinaryOp(
                        left,
                        operator,
                        right
                        )

        return left 

    def parse_expression_right() -> ast.Expression:
        left = parse_term() 
        while peek().text in ['+' , '-']: 
            operator_token = consume() 
            operator = operator_token.text 
            right = parse_expression_right() 
            left = ast.BinaryOp(
                    left, 
                    operator, 
                    right
                )

        return left

    def parse_parenthesized()-> ast.Expression:
        consume("(") 
        expr = parse_expression() 
        consume(")")
        return expr

    def parse_if() -> ast.Expression:
        if_token = consume("if") 
        condition= parse_expression() 

        then_token = consume("then") 
        then_condition = parse_expression() 
        
        el_branch = None 
        if peek().text == "else":
            consume("else") 
            el_branch = parse_expression()

        return ast.IfExpr(
                    condition=condition, 
                    then_branch = then_condition, 
                    else_branch = el_branch
                )
    return parse_expression() 




