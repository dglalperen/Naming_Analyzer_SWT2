# Variables
x = 10
y = '2023-05-24'

# Function
def f(a):
    """Calculate and return the average of a list of scores."""
    if a:
        return sum(a) / len(a)
    else:
        return 0

# Class
class A:
    """Representation of a student."""

    def __init__(self, b, c, d):
        self.b = b
        self.c = c
        self.d = d

    def e(self):
        """Calculate and return the average score of the student."""
        return f(self.d)

# Test functions
def g():
    assert f([1, 2, 3, 4, 5]) == 3

def h():
    i = A('John Doe', 20, [70, 80, 90])
    assert i.e() == 80
