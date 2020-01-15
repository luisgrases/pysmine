import copy
import inspect
from types import FunctionType
import sys

def when(fn):
    return fn


def describe(fn):
    return fn


def it(fn):
    return fn


def with_nested_specs(spec_case_class):
    import linecache

    linecache.clearcache()

    describe_decorators = _get_methods_with_decorator(spec_case_class, "describe")
    context_decorators = _get_methods_with_decorator(spec_case_class, "context")
    when_decorators = _get_methods_with_decorator(spec_case_class, "when")
    it_decorators = _get_methods_with_decorator(spec_case_class, "it")

    pyspec_decorators = (
        describe_decorators + context_decorators + when_decorators + it_decorators
    )

    to_execute = []

    def build_spec(parent):
        for inner_const in parent.__code__.co_consts:
            if hasattr(inner_const, "co_name") and (
                inner_const.co_name in pyspec_decorators
            ):
                new_parent = FunctionType(
                    inner_const,
                    parent.__globals__,
                    inner_const.co_name,
                    parent.__defaults__,
                    parent.__closure__,
                )
                to_execute.append(new_parent)
                build_spec(new_parent)
                to_execute.pop()

        if parent.__code__.co_name in it_decorators:
            x = copy.deepcopy(to_execute)

            def spec_to_execute(self):
                for func_to_ex in x:
                    func_to_ex(self)

            def get_func_name(func):
                return func.__code__.co_name

            setattr(
                spec_case_class,
                "test__" + "__".join(map(get_func_name, x)),
                _rename_code_object(spec_to_execute, parent.__code__.co_name),
            )

    for method in dir(spec_case_class):
        if method in pyspec_decorators:
            new_func = getattr(spec_case_class, method)
            to_execute.append(new_func)
            build_spec(new_func)
            to_execute.pop()

    return spec_case_class


def _get_methods_with_decorator(cls, decoratorName):
    sourcelines = inspect.getsourcelines(cls)[0]
    result = []
    for i, line in enumerate(sourcelines):
        line = line.strip()
        if line.split("(")[0].strip() == "@" + decoratorName:  # leaving a bit out
            nextLine = sourcelines[i + 1]
            name = nextLine.split("def ")[1].split("(")[0].strip()
            result.append(name)
    return result


def _rename_code_object(func, new_name):
    if sys.version_info > (3, 0):

        code_object = func.__code__
        function, code = type(func), type(code_object)
        return function(
            code(
                code_object.co_argcount,
                code_object.co_kwonlyargcount,
                code_object.co_nlocals,
                code_object.co_stacksize,
                code_object.co_flags,
                code_object.co_code,
                code_object.co_consts,
                code_object.co_names,
                code_object.co_varnames,
                code_object.co_filename,
                new_name,
                code_object.co_firstlineno,
                code_object.co_lnotab,
                code_object.co_freevars,
                code_object.co_cellvars,
            ),
            func.__globals__,
            new_name,
            func.__defaults__,
            func.__closure__,
        )
    else:
        raise Exception("BDD Only works with Python 3")
