from compiler.parser import parse
from compiler.ir_generator import generate_ir
from compiler.tokenizer import tokenize
from compiler.assembly_generator import *  
def test_expr():

    program = "var x = True; if x then 1 else 2;"
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

    asm = generate_assembly(ir_code) 
    print("\n") 
    for line in asm:
        print(line) 
 
if __name__ == "__main__":
    test_expr()
