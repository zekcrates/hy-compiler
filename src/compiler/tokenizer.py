import re 

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    line: int 
    column: int 

    def __eq__(self, other: object)-> bool  :
        if isinstance(other, SourceLocation) :
            return self.line == other.line and self.column == other.column 
        else:
            return True 

@dataclass(frozen=True) 
class Token:
    text: str 
    type: str 
    loc: SourceLocation 


ident_re = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
int_literal_re = re.compile(r'[0-9]+')
ws_re = re.compile(r'\s+')
pattern = r'[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|\s+'
def tokenize(source_code: str ) -> list[Token]: 
    
    tokens = re.findall(pattern, source_code)
    tokens = [t for t in tokens if not t.isspace() ]
    
    new_tokens: list[Token] =[]
    line = 1
    col = 1
    for token in tokens:
        if token == "\n":
            line +=1

            col +=1     
        else: 
            
            col +=1 
    

        token_type = None 
        if token.isdigit():
            token_type = "int_literal" 
        elif token.isalpha() or token.startswith("_") :
            token_type = "identifier" 
        else:
            token_type = "other" 

        new_token = Token(text=token, type=token_type, loc=SourceLocation(line=line, column=col))
        new_tokens.append(new_token) 
    print("new_tokens : " , new_tokens) 
    return new_tokens 



