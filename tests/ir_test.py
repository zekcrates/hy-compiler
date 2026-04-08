from compiler.parser import parse
from compiler.ir_generator import generate_ir
from compiler.tokenizer import tokenize
def test_expr():
    program = "print_int(1)"
    program = tokenize(program) 
    ast_root = parse(program)
    
    print("\n======== AST===========\n") 
    print(ast_root) 
    reserved = {"-", "*", "unary_-", "unary_not", "print_int", "print_bool" } 

    ir_code = generate_ir(reserved, ast_root)
    
    print("==== IR OUTPUT ====")
    for instr in ir_code:
        print(instr)

if __name__ == "__main__":
    test_expr()
