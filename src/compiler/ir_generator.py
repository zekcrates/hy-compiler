
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

    label_counter = 0
    def new_label(loc, prefix="L") -> ir.Label:
        nonlocal label_counter
        name = f"{prefix}{label_counter}"
        label_counter += 1
        return ir.Label(loc, name)
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
                var = new_var()
                instr = ir.Copy(loc, output, var) 
                ins.append(instr) 
                st.add_local(expr.name , var) 
                return var 

            case ast.Function():
                arg_vals   = []
                if expr.args is not None:
                    for arg in expr.args :

                        output = visit(st, arg) 
                        arg_vals.append(output) 
                var = new_var()
                fun_var = st.require(expr.name) 

                instr = ir.Call(loc, fun_var, arg_vals, var) 
                ins.append(instr) 
                return var 
            
            case ast.IfExpr():
                cond_var = visit(st, expr.condition) 
                then_label = new_label(loc, "then") 
                else_label = new_label(loc, "else") 
                end_label = new_label(loc, "if_end") 
                result_var = new_var() 

                instr = ir.CondJump(loc, cond_var, then_label, else_label) 

                ins.append(instr) 

                #then 
                ins.append(then_label) 
                then_val = visit(st, expr.then_branch) 
                ins.append(ir.Copy(loc, then_val , result_var)) 
                ins.append(ir.Jump(loc, end_label)) 

                #else 
                ins.append(else_label) 
                else_val = visit(st,expr.else_branch) 
                ins.append(ir.Copy(loc, else_val , result_var)) 
                ins.append(ir.Jump(loc, end_label)) 

                ins.append(end_label) 
                return result_var

    root_symtab = SymTab[IRVar](parent=None)
    for name in reserved_names:
        root_symtab.add_local(name, IRVar(name))

    var_final_result = visit(root_symtab, root_expr)

    if root_expr.type == Int:
        func = root_symtab.require("print_int") 
        var = new_var()
        instr = ir.Call(loc, func, [var_final_result] , var) 
        ins.append(instr) 
    
    elif root_expr.type == Bool:
        fucn = root_symtab.require("print_bool") 
        var = new_var() 
        instr = ir.Call(loc, func, [var_final_result] , var) 
        ins.append(instr) 


    return ins
