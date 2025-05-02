# -*- coding: utf-8 -*-


import contextlib


@contextlib.contextmanager
def ctx1():
    print("Acquiring Context 1 resource")
    try:
        yield 1
    finally:
        print("Releasing Context 1 resource")


@contextlib.contextmanager
def ctx2():
    print("Acquiring Context 2 resource")
    try:
        yield 2
    finally:
        print("Releasing Context 2 resource")


def func1(flag1: bool, flag2: bool):
    cm1 = ctx1() if flag1 else contextlib.nullcontext()
    cm2 = ctx2() if flag2 else contextlib.nullcontext()
    with cm1, cm2:
        print("Run core logic")
        raise Exception("Error in core logic")


def func2(flag1: bool, flag2: bool):
    with contextlib.ExitStack() as stack:
        cm1 = stack.enter_context(ctx1()) if flag1 else None
        cm2 = stack.enter_context(ctx2()) if flag2 else None
        print("Run core logic")
        raise Exception("Error in core logic")


def test1():
    # print("")
    # func1(flag1=True, flag2=True)
    # func1(flag1=True, flag2=False)
    # func1(flag1=False, flag2=True)
    # func1(flag1=False, flag2=False)
    pass


def test2():
    # print("")
    # func2(flag1=True, flag2=True)
    # func2(flag1=True, flag2=False)
    # func2(flag1=False, flag2=True)
    # func2(flag1=False, flag2=False)
    pass


if __name__ == "__main__":
    from cdk_mate.tests import run_unit_test

    run_unit_test(__file__)
