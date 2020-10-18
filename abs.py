from dataclasses import dataclass
from typing import Union, TypeVar

T = TypeVar('T')

@dataclass
class Type:
    value: str

@dataclass
class Id:
    value: str

@dataclass
class LitInt:
    value: int

@dataclass
class Neg:
    value: 'Expr'

@dataclass
class Plus:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Minus:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Expr:
    expr: Union[Id, LitInt, Neg, Plus, Minus]

@dataclass
class VarDef:
    expr: Expr
    typ: Type

@dataclass
class Assign:
    expr1: Expr
    expr2: Expr

@dataclass
class Stm:
    stm: Union[VarDef, Assign]

