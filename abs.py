from dataclasses import dataclass, field
from typing import Union, TypeVar

T = TypeVar('T')

@dataclass
class Type:
    value: str
    type: str = field(repr=False, default='Type')

@dataclass
class Id:
    value: str
    type: str = field(repr=False, default='Id')

@dataclass
class LitInt:
    value: int
    type: str = field(repr=False, default='LitInt')

@dataclass
class Neg:
    value: 'Expr'
    type: str = field(repr=False, default='Neg')

@dataclass
class Plus:
    left: 'Expr'
    right: 'Expr'
    type: str = field(repr=False, default='Plus')

@dataclass
class Minus:
    left: 'Expr'
    right: 'Expr'
    type: str = field(repr=False, default='Minus')

@dataclass
class Expr:
    expr: Union[Id, LitInt, Neg, Plus, Minus]
    type: str = field(repr=False, default='Expr')

@dataclass
class VarDef:
    expr: Expr
    typ: Type
    type: str = field(repr=False, default='VarDef')

@dataclass
class Assign:
    expr1: Expr
    expr2: Expr
    type: str = field(repr=False, default='Assign')

@dataclass
class Stm:
    stm: Union[VarDef, Assign]
    type: str = field(repr=False, default='Stm')

