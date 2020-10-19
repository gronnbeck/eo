from dataclasses import dataclass
from typing import Union, Dict
import abs

EnvType = Union[int]

@dataclass
class Env:
    value: Dict[str, EnvType]

def env_add(env: Env, id: str, value: EnvType) -> None:
    env.value[id] = value

def env_lookup(env: Env, id: str) -> EnvType:
    return env.value[id]

@dataclass
class Eval:
    env: Env

def eval_new():
    return Eval(env=Env(value={}))

def eval_print_env(e: Eval):
    print('Environment {}'.format(e.env))

def eval_exec_stm(e: Eval, stm: abs.Stm) -> None:
    if isinstance(stm, abs.VarDef):
        return
    elif isinstance(stm, abs.Assign):
        if isinstance(stm.expr1, abs.Id):
            s = stm.expr1.value
            x = eval_(e, stm.expr2)
            env_add(e.env, s, x)
            return
    raise Exception('Panic: Unknown stm: {} in exec'.format(stm))

def eval_(e: Eval, expr: abs.Expr) -> EnvType:
    if isinstance(expr, abs.Id):
        return env_lookup(e.env, expr.value)
    elif isinstance(expr, abs.LitInt):
        return expr.value
    elif isinstance(expr, abs.Neg):
        return -1 * eval_(e, expr.value)
    elif isinstance(expr, abs.Plus):
        return eval_(e, expr.left) + eval_(e, expr.right)
    elif isinstance(expr, abs.Minus):
        return eval_(e, expr.left) - eval_(e, expr.right)
    else:
        raise Exception('Unknown expression: {}'.format(expr))


