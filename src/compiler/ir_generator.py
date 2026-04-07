
from compiler import ast, ir
#from compiler.symtab import SymTab
from compiler.types import Bool, Int, Unit
from compiler.ir import * 
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")

@dataclass
class SymTab(Generic[T]):
    parent: Optional["SymTab[T]"] = None

    def __post_init__(self):
        self.locals: Dict[str, T] = {}

    def add_local(self, name: str, value: T) -> None:
        self.locals[name] = value

    def lookup(self, name: str) -> Optional[T]:
    
        if name in self.locals:
            return self.locals[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        return None

    def require(self, name: str) -> T:
        
        value = self.lookup(name)
        if value is None:
            raise Exception(f"Undefined variable: {name}")
        return value
    
def generate_ir(
    reserved_names: set[str],
    root_expr: ast.Expression
) -> list[ir.Instruction]:
    var_unit = IRVar('unit')
    
    counter = 0 
    def new_var() -> IRVar:
        nonlocal counter 
        name = f"v{counter}"
        counter +=1 
        return IRVar(name) 
    ins: list[ir.Instruction] = []

    def visit(st: SymTab[IRVar], expr: ast.Expression) -> IRVar:
        loc = expr.location

        match expr:
            case ast.Literal():
                match expr.value:
                    case bool():
                        var = new_var()
                        ins.append(ir.LoadBoolConst(
                            loc, expr.value, var))
                    case int():
                        var = new_var()
                        ins.append(ir.LoadIntConst(
                            loc, expr.value, var))
                    case None:
                        var = var_unit
                    case _:
                        raise Exception(f"{loc}: unsupported literal: {type(expr.value)}")

                return var

            case ast.Identifier():
                return st.require(expr.name)
            
            case ast.BinaryOp():
                var_op = st.require(expr.op)

                left = visit(st,expr.left) 
                right = visit(st,expr.right)
                var_result = new_var()
                instr  = ir.Call(loc, var_op, [left,right], var_result) 
                ins.append(instr) 

                return var_result 
            
            case ast.UnaryOp():
                var_op = st.require('unary_'+ expr.op) 
                var_result = new_var() 
                value = visit(st, expr.expr) 

                instr = ir.Call(loc, var_op, [value], var_result) 
                ins.append(instr) 

                return var_result 

            case ast.VarDecl():
                output = visit(st, expr.value) 
                st.add_local(name, IRVar(output))
                var = new_var()


    root_symtab = SymTab[IRVar](parent=None)
    for name in reserved_names:
        root_symtab.add_local(name, IRVar(name))

    var_final_result = visit(root_symtab, root_expr)
    return ins
