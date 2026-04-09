from compiler.parser import parse
from compiler.ir_generator import generate_ir
from compiler.tokenizer import tokenize
from compiler.assembly_generator import Locals , get_all_ir_variables 
def test_expr():

    program = "print_int(1)"
    program = tokenize(program) 
    ast_root = parse(program)
    
    print("\n======== AST===========\n") 
    print(ast_root) 
    reserved = {"-", "*", "unary_-", "unary_not", "print_int", "print_bool" } 

    
    ir_code = generate_ir(reserved, ast_root)
    print("\nir code \n") 
    for i in ir_code:
        print(ir_code) 
    l = Locals(get_all_ir_variables(ir_code)) 
    print("\nlocals\n")
    print(l._var_to_location) 
    print(l._stack_used) 
if __name__ == "__main__":
    test_expr()
