from __future__ import annotations
from typing import List

class IntType:
    def __repr__(self) -> str:
        return "Int"

class BoolType:
    def __repr__(self) -> str:
        return "Bool"

class UnitType:
    def __repr__(self) -> str:
        return "Unit"

Int = IntType()
Bool = BoolType()
Unit = UnitType()

#Type = IntType | BoolType | UnitType | 'FunctionType'

class FunctionType:
    def __init__(self, param_types: List[IntType | BoolType | UnitType], return_type: IntType | BoolType | UnitType) -> None:
        self.param_types = param_types
        self.return_type = return_type

    def __repr__(self) -> str:
        return f"({self.param_types} -> {self.return_type})"


Type = IntType | BoolType | UnitType | FunctionType
