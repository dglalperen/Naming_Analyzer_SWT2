# Variables
num_of_students = 10
current_date = '2023-05-24'

# Function
def calculate_average(scores):
    """Calculate and return the average of a list of scores."""
    if scores:
        return sum(scores) / len(scores)
    else:
        return 0

# Class
class Student:
    """Representation of a student."""

    def __init__(self, name, age, scores):
        self.name = name
        self.age = age
        self.scores = scores

    def get_average_score(self):
        """Calculate and return the average score of the student."""
        return calculate_average(self.scores)

# Another class
class Course:
    """Representation of a course."""

    def __init__(self, name, students):
        self.name = name
        self.students = students

    def get_average_course_score(self):
        """Calculate and return the average score of all students in the course."""
        all_scores = [student.get_average_score() for student in self.students]
        return calculate_average(all_scores)

# Test functions
def test_calculate_average():
    assert calculate_average([1, 2, 3, 4, 5]) == 3

def test_student_average_score():
    student = Student('John Doe', 20, [70, 80, 90])
    assert student.get_average_score() == 80

def test_course_average_score():
    students = [Student('John Doe', 20, [70, 80, 90]), Student('Jane Doe', 19, [80, 90, 100])]
    course = Course('Math', students)
    assert course.get_average_course_score() == 85
