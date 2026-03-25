import re 


ident_re = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
int_literal_re = re.compile(r'[0-9]+')
ws_re = re.compile(r'\s+')
pattern = r'[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|\s+'
def tokenize(source_code: str ) -> list[str]: 
    
    tokens = re.findall(pattern, source_code)
    tokens = [t for t in tokens if not t.isspace() ] 
    print("tokens : ", tokens) 
    return tokens 



tokenize("if while true\n i=10")

