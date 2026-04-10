import compiler.ir as ir  
import dataclasses 

class Locals:
    _var_to_location: dict[ir.IRVar, str]= {} 
    _stack_used: int 
    
    def __init__(self, variables: list[ir.IRVar]) -> None:
        rbp = "(%rbp)" 
        count = 8 
        for var in variables:
            self._var_to_location[var] = str(-count)+rbp
            count+=8 

        
        self._stack_used = 8 * len(self._var_to_location.keys()) 


    def get_ref(self, v:ir.IRVar) -> str:
        return self._var_to_location[v] 

    def stack_used(self) -> int: 
        return self._stack_used



def get_all_ir_variables(instructions: list[ir.Instruction]) -> list[ir.IRVar]: 
    result_list: list[ir.IRVar] = []
    result_set: set[ir.IRVar] = set()

    def add(v: ir.IRVar) -> None:
        if v not in result_set:
            result_list.append(v) 
            result_set.add(v) 

    for insn in instructions:
        for field in dataclasses.fields(insn):
            value = getattr(insn, field.name) 
            if isinstance(value ,ir.IRVar) :
                add(value) 

            if isinstance(value, list) :
                for v in value:
                    if isinstance(v , ir.IRVar):
                        add(v) 
    return result_list 

def generate_assembly(instructions: list[ir.Instruction]) -> list[str]:
    lines: list[str] = []
    def emit(line: str) -> None: lines.append(line)

    locals = Locals(
        variables=get_all_ir_variables(instructions)
    )

    emit("pushq  %rbp")
    emit("movq   %rsp, %rbp")
    emit("subq   ${local._stack_used}, %rsp ")
    for insn in instructions:
        emit('# ' + str(insn)) 

        
        match insn:
            case ir.Label():
                emit("")
                emit(f".L{insn.name}") 

            case ir.LoadIntConst():
                if -2**31 <= insn.value <= 2**31:
                    emit(f"movq {insn.value} , {locals.get_ref(insn.dest)}")
            

            case ir.LoadBoolConst():
                if insn.value == True:
                    emit(f"movq 1 , {locals.get_ref(insn.dest)}") 
                else:
                    emit(f"movq 0 , {locals.get_ref(insn.dest)}") 
            
            case ir.Copy():
                emit(f"movq {locals.get_ref(insn.source)}, %rax") 
                emit(f"movq %rax , {locals.get_ref(insn.dest)} " ) 

        
            case ir.Jump():
                emit(f"jmp {insn.label.name}")
            case ir.Call():
                args = insn.args 
                arg_regs = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
                
                for i, arg in enumerate(args):
                    if i >= len(arg_regs):
                        raise Exception("Too many arguments (max 6 supported)")
                    emit(f"movq {locals.get_ref(arg)}, {arg_regs[i]}")

                emit(f"call {insn.fn.name}")
                emit(f"movq %rax, {locals.get_ref(insn.dest)}")
            case ir.CondJump():
                emit(f"cmpq $0 , {locals.get_ref(insn.cond)} ") 
                emit(f"jne {locals.get_ref(insn.then_label}")
                emit(f"jmp {locals.get_ref(insn.else_label}")


        
        emit("movq %rbp, %rsp")
        emit("popq %rbp")
        emit("ret")
    return lines 
