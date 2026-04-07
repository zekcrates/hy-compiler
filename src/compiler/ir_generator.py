
from compiler import ast, ir
from compiler.symtab import SymTab
from compiler.types import Bool, Int, Unit

def generate_ir(
    reserved_names: set[str],
    root_expr: ast.Expr
) -> list[ir.Instruction]:
    var_unit = IRVar('unit')

    def new_var() -> IRVar:
        pass 
    ins: list[ir.Instruction] = []

    def visit(st: SymTab[IRVar], expr: ast.Expr) -> IRVar:
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


    root_symtab = SymTab[IRVar](parent=None)
    for name in reserved_names:
        root_symtab.add_local(name, IRVar(name))

    var_final_result = visit(root_symtab, root_expr)
    return ins
