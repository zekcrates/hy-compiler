

class IntType:
    def __repr__(self):
        return "Int" 

class BoolType:
    def __repr__(self):
        return "Bool"

class UnitType:
    def __repr__(self):
        return "Unit"


Int = IntType()
Bool = BoolType()
Unit = UnitType()

Type = Int | Bool | Unit 

class FunctionType:
    def __init__(self, from_type, to_type) :
        self.from_type = from_type 
        self.to_type = to_type 

    def __repr__(self):
        return f"({self.from_type} -> {self.to_type})"
