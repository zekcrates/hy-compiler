from compiler.tokenizer import tokenize, Token, SourceLocation

class AnyLocation(SourceLocation): 
    def __eq__(self, other:object)->bool :
        return True 

L = AnyLocation(0,0)

#def test_tokenizer_basics() -> None:
 #   assert tokenize("if  3\nwhile") == ['if', '3', 'while']
  #  assert tokenize("while true i  ") == ['while', 'true', 'i'] 


def test_tokenizer_task2() -> None:
    assert tokenize('aaa 123 bbb') == [
    Token(loc=L, type="identifier", text="aaa"),
    Token(loc=L, type="int_literal", text="123"),
    Token(loc=L, type="identifier", text="bbb"),
    ]

