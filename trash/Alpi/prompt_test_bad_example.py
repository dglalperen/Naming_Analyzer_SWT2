x = 10
y = "2023-05-24"


def f(a):
    if a:
        return sum(a) / len(a)
    else:
        return 0


class A:
    def __init__(self, b, c, d):
        self.b = b
        self.c = c
        self.d = d

    def e(self):
        return f(self.d)


def g():
    assert f([1, 2, 3, 4, 5]) == 3


def h():
    i = A("John Doe", 20, [70, 80, 90])
    assert i.e() == 80
