#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path
import ast
import inspect
import traceback


# Variables ===================================================================
# Functions & classes =========================================================
bigus_dictus = {
    "r:import": {
        "@xmlns:r": "http://resolver.nkp.cz/v3/",
        "r:monograph": {
            "r:titleInfo": {
                "r:title": "asdad",
            },
            "r:primaryOriginator": {
                "@type": "AUTHOR",
                "#text": "asd"
            },
        },
    }
}


def xex(asd=1, bsd=2, aaa=3):
    print traceback.print_stack()
    return {
        "r:import": {
            "@xmlns:r": "http://resolver.nkp.cz/v3/",
            "r:monograph": {
                "r:titleInfo": {
                    "r:title": asd,
                },
                "r:primaryOriginator": {
                    "@type": "AUTHOR",
                    "#text": bsd
                },
            },
        }
    }

# xex()
# tree = ast.parse(inspect.getsource(xex))

# for el in ast.walk(tree):
    # print el


def _disable_nested_calls(func_name, args_ast):
    for arg in args_ast:
        for el in ast.walk(arg):
            if not isinstance(el, ast.Call):
                continue

            if not hasattr(el.func, "id"):
                continue

            if el.func.id == func_name:
                raise ValueError(
                    "Sorry, nested calls are not supported!\n"
                    "All dicts are converted by default."
                )


def _match_by_lineno(func_name, known_fn, list_of_unknown):
    for candidate in list_of_unknown:
        _disable_nested_calls(func_name, candidate.args)

    candidates = filter(lambda x: x.lineno <= known_fn.lineno, list_of_unknown)

    if candidates:
        return max(candidates, key=lambda x: x.lineno)

    raise ValueError("Couldn't identify matching fuction.")


# Možná jen resortovat výstupní OrderedDict na základě pořadí klíčů ve vstupním?
# Nedovolit zanořené cally order()u, tím se eliminuje problém s jeho korektním
# vyhledáním
# 
# Detekce dvou funkcí na jednom řádku


def order(input_dict):
    if not isinstance(input_dict, dict):
        raise ValueError("`input_dict` have to be instance of `dict`.")

    # TODO: this may fuck the 'from import ..' functionality
    frame = inspect.currentframe()

    # get name of current function
    func_name = inspect.getframeinfo(frame).function

    # this helps to reduce lookup complexity
    first_line = frame.f_back.f_code.co_firstlineno

    # get outer frames
    outer_frames = inspect.getouterframes(inspect.currentframe())
    if len(outer_frames) <= 1:
        raise ValueError("Can't inspect outer frame!")

    # select proper outer frame
    frame_info = inspect.getframeinfo(outer_frames[1][0])

    # TODO: remove this data example
    # Traceback(filename='./ast_test.py', lineno=84, function='whops', code_context=['                    "#text": "asd"\n'], index=0)

    # parse the file from which the function call originated
    if not os.path.exists(frame_info.filename):
        raise IOError("Can't open '%s'!" % frame_info.filename)

    with open(frame_info.filename) as f:
        source = f.read()

    tree = ast.parse(source, frame_info.filename)

    # get AST nodes for function call to function with `func_name` name
    func_calls = filter(
        lambda x:
            isinstance(x, ast.Call) and
            hasattr(x.func, "id") and
            x.func.id == func_name,
        ast.walk(tree)
    )

    # filter functions with lineno <= than lineno of frame_info (inspect
    # returns LAST active line of function call, ast returns FIRST line - we
    # need to match those)
    func_calls = filter(
        lambda x: x.lineno <= frame_info.lineno and x.lineno >= first_line,
        func_calls
    )

    if not func_calls:
        raise ValueError("Couldn't find the %s call!" % func_name)

    matching_fn = _match_by_lineno(func_name, frame_info, func_calls)

    print matching_fn.lineno, matching_fn.func.id


def return_xex():
    pass

def whops():
    a = "asd"
    order({"azgabash": a})

    order({
        "r:import": {
            "@xmlns:r": "http://resolver.nkp.cz/v3/",
            "r:monograph": {
                "r:titleInfo": {
                    "r:title": return_xex(
                    ),
                },
                "r:primaryOriginator": {
                    "@type": "AUTHOR",
                    "#text": {"asd":"bsd"}
                },
            },
        }
    })

    order({"asd": "xerexin"})

    return_xex()

whops()
