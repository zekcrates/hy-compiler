from compiler.tokenizer import tokenize

def test_tokenizer_basics() -> None:
    assert tokenize("if  3\nwhile") == ['if', '3', 'while']
    assert tokenize("while true i  ") == ['while', 'true', 'i'] 


