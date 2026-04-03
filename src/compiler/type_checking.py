import compiler.ast as ast 
from compiler.types import Int, Type, Bool, FunctionType, Unit 



class SymTab:
    def __init__(self, parent=None) :
        self.locals: dict[str, Type] = {}
        self.parents: SymTab | None = parent 


def new_table() -> SymTab:
        top = SymTab()
        top.locals['+'] = Int 
        top.locals['-'] = Int 
        top.locals['*'] = Int 
        top.locals['/'] = Int 
        top.locals['<'] = Bool 
        top.locals['>'] = Bool 
        top.locals['<='] = Bool 
        top.locals['>='] = Bool 
        top.locals['print_int'] = FunctionType(Int, Unit)  
        top.locals['print_bool'] = FunctionType(Bool, Unit) 
        return top 
def typecheck(node: ast.Expr, symtab: SymTab) -> Type:
    match node: 
        case ast.BinaryOp():
            t1 = typecheck(node.left, symtab)
            t2 = typecheck(node.right, symtab) 
            if node.op == "+":
                if t1 is not Int or t2 is not Int:
                    raise Exception("Wrong type" )

        case ast.IfThen():
            cond = typecheck(node.condition, symtab) 
            if cond is not Bool:
                raise Exception("Wrong type for bool") 
            then = typecheck(node.then_branch, symtab) 
            else_b = None
            if node.else_branch is not None:

                else_b = typecheck(node.else_branch, symtab) 
            if else_b is not None and then != else_b:
                raise Exception("Wrong type condition") 
            return then 
        
        case ast.Literal():
            return Int 

        case VarDecl():
            name = node.name 
            val = typecheck(node.value, symtab) 
            symtab.locals[name] = val 
            return val 


        case ast.Identifier():
            return lookup(node.name , symtab) 

        case _:
            raise Exception(f"Unsupported node type: (type(node).__name__}")        

        return False

def lookup(name: str, symtab: SymTab) -> Type: 
    if name in symtab.locals:
        return symtab.locals[name] 
    elif symtab.parent is not None:
        return lookup(name ,symtab.parent) 
    else:
        raise Exception(f"Undefined type for variable {name}") 
