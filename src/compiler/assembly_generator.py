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

def generate_assembly(instructions: list[ir.Instruction]) -> str:
    lines = []
    def emit(line: str) -> None: lines.append(line)

    locals = Locals(
        variables=get_all_ir_variables(instructions)
    )


    for insn in instructions:
        emit('# ' + str(insn)) 

            
