from compiler.tokenizer import Token 
import compiler.ast as ast 


operators = ['+', '-', '%', '==','!=', '<', '<=', '>', '>=', 'and' , 'or' ,'-', 'not'  ]

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

    def parse_assignment() ->ast.Expression:
        left = parse_or() 
        if peek().text == "=":
            consume("=") 
            value = parse_assignment() 
            left = ast.Assignment(left, value) 
        return left
    def parse_or() ->ast.Expression:
        left = parse_and() 
        while peek().text == "or":
            operator_token = consume() 
            operator = operator_token.text 
            right =parse_and() 
            left = ast.BinaryOp(left, operator, right)
        return left
    def parse_and() -> ast.Expression:
        left = parse_equality() 
        while peek().text == 'and':
            operator_token = consume() 
            operator = operator_token.text 
            right = parse_equality() 
            left = ast.BinaryOp(left, operator, right) 
        return left 
    def parse_equality() -> ast.Expression:
        left = parse_comparison() 
        while peek().text in ['==', '!=']: 
            operator_token = consume() 
            operator = operator_token.text 
            right = parse_equality() 
            left = ast.BinaryOp(left,operator, right)

        return left 
    def parse_comparison() -> ast.Expression:
        left = parse_expression()
        while peek().text in ["<" ,"<=" , ">" , ">="]:
            operator_token = consume() 
            operator = operator_token.text
            right = parse_expression() 
            left = ast.BinaryOp(left, operator, right)
        return left 


    def parse_int_literal() -> ast.Literal:
        if peek().type != "int_literal":
            raise Exception(f'{peek().loc}: expected an integer literal')
        token = consume() 
        return ast.Literal(int(token.text)) 
    

    def parse_identifier() -> ast.Expression:
        if peek().type != "identifier" :
            
            raise Exception(f'{peek().loc}: expected an identifier')
        token = consume()

        # checking for function 
        if peek().text == "(":
            return parse_function(token) 
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
        left = parse_unary() 

        while peek().text in ['*','/', '%']:
            operator_token = consume() 
            operator = operator_token.text 
            right = parse_unary()
            left = ast.BinaryOp(
                        left,
                        operator,
                        right
                        )

        return left 
    
    def parse_unary() -> ast.Expression:
        if peek().text in ['-', 'not']:
            operator_token = consume() 
            operator = operator_token.text 
            expr = parse_unary() 
            return ast.UnaryOp(operator, expr)
        return parse_factor()
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

    def parse_function(fname_token: Token) -> ast.Expression:
        #(a,b) 
        name = fname_token.text
        consume("(") 
        args: list[ast.Expression] =[]
        
        if peek().text != ")":
            args.append(parse_expression()) 
            while peek().text == ',':
                consume(",") 
                args.append(parse_expression())

            consume(")")

        return ast.Function(name=name , args=args if len(args) > 0 else None) 

    def parse_if() -> ast.Expression:
        if_token = consume("if") 
        condition= parse_or() 

        then_token = consume("then") 
        then_condition = parse_or()
        
        el_branch = None 
        if peek().text == "else":
            consume("else") 
            el_branch = parse_or()

        return ast.IfExpr(
                    condition=condition, 
                    then_branch = then_condition, 
                    else_branch = el_branch
                )
    return parse_assignment() 




