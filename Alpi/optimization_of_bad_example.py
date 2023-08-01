from typing import List

x = 10
target_date = "2023-05-24"


def calculate_average(numbers: List[float]) -> float:
    """
    Calculates the average of a list of numbers.
    """
    if numbers:
        return sum(numbers) / len(numbers)
    else:
        return 0


class MyClass:
    def __init__(self, name: str, age: int, grades: List[float]):
        self.name = name
        self.age = age
        self.grades = grades

    def calculate_grade_average(self) -> float:
        """
        Calculates the average grade for the student.
        """
        return calculate_average(self.grades)


def test_calculate_average():
    """
    Tests the calculate_average function.
    """
    assert calculate_average([1, 2, 3, 4, 5]) == 3


def test_class_method():
    """
    Tests the calculate_grade_average method of MyClass.
    """
    student = MyClass("John Doe", 20, [70, 80, 90])
    assert student.calculate_grade_average() == 80
