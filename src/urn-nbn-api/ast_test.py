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


def _disable_nested_calls(args_ast):
    for arg in args_ast:
        for el in ast.walk(arg):
            if isinstance(el, ast.Call):
                raise ValueError("Sorry, nested calls are not supported!")


def _same_args_naive(input_dict, ast_args):
    if len(ast_args) > 1:
        return False

    ser = ast.parse(repr(input_dict))

    if ast.dump(ser.body[0].value) == ast.dump(ast_args[0]):
        return True

    return False


def _same_args(input_dict, ast_args):
    pass


def _with_same_args(known_fn, input_dict, list_of_unknown):
    list_of_unknown = sorted(list_of_unknown, key=lambda x: x.lineno)

    for candidate in list_of_unknown:
        _disable_nested_calls(candidate.args)

        if _same_args_naive(input_dict, candidate.args):
            return candidate

        if _same_args(input_dict, candidate.args):
            return candidate

    return None  # TODO: Remove

    raise ValueError("Couldn't identify matching fuction.")


# Možná jen resortovat výstupní OrderedDict na základě pořadí klíčů ve vstupním?
# Nedovolit zanořené cally order()u, tím se eliminuje problém s jeho korektním
# vyhledáním


def order(input_dict):
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

    # select proper function call - inspect's frameinfo returns name of last
    # active function call line, but ast expects first line of the function
    # call
    # for el in func_calls:
    #     print el, el.lineno, el.func.id
    #     print el.args[0].keys
    #     # print dir(el)
    #     print ast.dump(el)
    #     print
    print "looking for line", frame_info.lineno, func_name, frame_info.code_context
    matching_fn = _with_same_args(frame_info, input_dict, func_calls)
    print "\t", matching_fn

    # print matching_fn.lineno, matching_fn.func.id


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
                "r:primaryOriginator": order({
                    "@type": "AUTHOR",
                    "#text": order({"asd":"bsd"})
                }),
            },
        }
    })

    order({"asd": "xerexin"})

    return_xex()

whops()
