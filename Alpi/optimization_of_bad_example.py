x = 10
target_date = "2023-05-24"


def calculate_average(numbers):
    if numbers:
        return sum(numbers) / len(numbers)
    else:
        return 0


class MyClass:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades

    def calculate_grade_average(self):
        return calculate_average(self.grades)


def perform_assertion():
    assert calculate_average([1, 2, 3, 4, 5]) == 3


def execute_example():
    instance = MyClass("John Doe", 20, [70, 80, 90])
    assert instance.calculate_grade_average() == 80


# {
#     "score": "0.7"
# }
