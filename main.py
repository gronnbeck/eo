import sys
import re
from dataclasses import dataclass
from typing import List

import abs

@dataclass
class Line:
    content: str

@dataclass
class ParseRule:
    name: str
    regex: str

@dataclass
class Parser:
    rules: List[ParseRule]

def parser():
    id = '([a-z]+)'
    typ = '([A-Z]{1}[a-z]*)'
    litint = '([0-9]+)'
    expr = '(.*)'

    parse_patterns = [
        ('Vardef', [id, ' :: ', typ]),
        ('Assign', [id, ' = ', expr]),
        ('Type', [typ]),
        ('Id', [id]),
        ('LitInt', [litint]),
        ('Plus', [expr, ' \+ ', expr]),
        ('Minus', [expr, ' \- ', expr]),
        ('Neg', ['\-', expr]),
    ]

    rules = []
    for name, pattern_parts in parse_patterns:
        regex_str = '^'
        for part in pattern_parts:
            regex_str = regex_str + part
        regex_str = regex_str + '$'
        rule = ParseRule(name=name, regex=regex_str)
        rules.append(rule)

    return Parser(rules=rules)

def parse(parser, lines):
    stmts = []
    for line in lines:
        l = parse_stm(parser, line.content)
        stmts.append(l)
    return stmts

def parse_stm(parser, line):
    for rule in parser.rules:
        if re.match(rule.regex, line):
            c = re.search(rule.regex, line)
            if rule.name == 'Vardef':
                return vardef(parser, c)
            elif rule.name == 'Assign':
                return assign(parser, c)
            else:
                raise Exception('Bad match: ' + rule.name)
    raise Exception('No match: ' + line)

def vardef(parser, cap):
    expr = parse_expr(parser, cap.group(1))
    typ = cap.group(2)
    return abs.VarDef(expr, abs.Type(typ))

def assign(parser, cap):
    expr1 = parse_expr(parser, cap.group(1))
    expr2 = parse_expr(parser, cap.group(2))
    return abs.Assign(expr1, expr2)

def parse_expr(parser, line):
    for rule in parser.rules:
        if re.match(rule.regex, line):
            c = re.search(rule.regex, line)
            if rule.name == 'Id':
                return id(c)
            elif rule.name == 'LitInt':
                return litint(c)
            elif rule.name == 'Neg':
                return neg(parser, c)
            elif rule.name == 'Plus':
                return plus(parser, c)
            elif rule.name == 'Minus':
                return minus(parser, c)
            else:
                raise Exception('Bad match: ' + rule.name)
    raise Exception('No match: "{}"'.format(line))

def id(cap):
    s = cap.group(1)
    return abs.Id(s)

def litint(cap):
    i = int(cap.group(1))
    return abs.LitInt(1)

def neg(parser, cap):
    expr = parse_expr(parser, cap.group(1))
    return abs.Neg(expr)

def plus(parser, cap):
    expr1 = parse_expr(parser, cap.group(1))
    expr2 = parse_expr(parser, cap.group(2))
    return abs.Plus(expr1, expr2)

def minus(cap):
    expr1 = parse_expr(parser, cap.group(1))
    expr2 = parse_expr(parser, cap.group(2))
    return abs.Minus(expr1, expr2)

def process(x):
    if x == '\n':
        return None
    return Line(content=x)

def preprocessor(s):
    lines = s.readlines()
    return list(filter(lambda x: x != None, map(process, lines)))

import dataclasses, json

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

def main():
    args = sys.argv
    if len(args) < 2:
        raise Exception('Please provide a file')
    path = args[1]
    s = open(path, 'r')

    p = parser()
    lines = preprocessor(s)
    stms = parse(p, lines)
    print('Parsed: ' + json.dumps(stms, cls=EnhancedJSONEncoder))

if __name__ == '__main__':
    main()
