#!/usr/bin/python3.9 -u

from sys import modules, argv
del modules['os']
from mutuple import append
keys = list(__builtins__.__dict__.keys())

from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import full_write_guard

from operator import getitem

def _inplacevar_(op, var, expr):
    if op == "+=":
            return var + expr
    elif op == "-=":
            return var - expr
    elif op == "*=":
        return var * expr
    elif op == "/=":
        return var / expr
    elif op == "%=":
        return var % expr
    elif op == "**=":
        return var ** expr
    elif op == "<<=":
        return var << expr
    elif op == ">>=":
        return var >> expr
    elif op == "|=":
        return var | expr
    elif op == "^=":
        return var ^ expr
    elif op == "&=":
        return var & expr
    elif op == "//=":
        return var // expr
    elif op == "@=":
        return var // expr

filename = argv[1]

with open(f"/tmp/{filename}", "r") as file:
    builtins = safe_builtins

    builtins["_getitem_"] = getitem
    builtins["_getiter_"] = default_guarded_getiter
    builtins["_inplacevar_"] = _inplacevar_
    builtins["_write_"] = full_write_guard
    builtins["bytes"] = bytes
    builtins["chr"] = chr
    builtins["input"] = input
    builtins["append"] = append
    builtins["ord"] = ord
    builtins["print_"] = print # allow printing in sandbox
    builtins["type"] = type

    exec(
        compile_restricted(file.read(), filename="<inline-code>", mode="exec"),
        {"__builtins__": builtins},
        None
    )
