# Variables
n_students = 10
date_now = '2023-05-24'

# Function
def avg_calc(s_list):
    """Calculate and return the average of a list of scores."""
    if s_list:
        return sum(s_list) / len(s_list)
    else:
        return 0

# Class
class Pupil:
    """Representation of a student."""

    def __init__(self, pupil_name, pupil_age, pupil_scores):
        self.pupil_name = pupil_name
        self.pupil_age = pupil_age
        self.pupil_scores = pupil_scores

    def get_avg_s(self):
        """Calculate and return the average score of the student."""
        return avg_calc(self.pupil_scores)

# Test functions
def test_avg_calc():
    assert avg_calc([1, 2, 3, 4, 5]) == 3

def test_pupil_avg_s():
    pupil_obj = Pupil('John Doe', 20, [70, 80, 90])
    assert pupil_obj.get_avg_s() == 80
