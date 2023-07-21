import functools


def aaa(a, b, c, d):
    print(a, b, c, d)


functools.partial(aaa, 2, 3, 4)(1)
