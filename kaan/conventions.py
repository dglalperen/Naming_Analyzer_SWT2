import re
import nltk
import unittest
from nltk.corpus import words

# Download the 'words' corpus from nltk
nltk.download('words')

# Create a set of English words for later use
english_words = set(words.words())

# Function to split a compound word into its constituents
def split_compound_word(word):
    word = word.lower()
    split_words = []
    while len(word) > 0:
        max_len_word = ''
        for i in range(len(word)):
            if word[:i+1] in english_words and len(word[:i+1]) > len(max_len_word):
                max_len_word = word[:i+1]
        if max_len_word != '':
            split_words.append(max_len_word)
            word = word[len(max_len_word):]
        else:
            break
    return split_words

# Define the PEP 8 naming conventions for different types of identifiers
pep8_naming_conventions = {
    "function": r"^[a-z_][a-z0-9_]{2,30}$",
    "class": r"^[A-Z][a-zA-Z0-9]{2,30}$",
    "variable": r"^[a-z_][a-z0-9_]{2,30}$",
    "constant": r"^[A-Z_][A-Z0-9_]{2,30}$",
}

# Function to check if a given name is conformant with a given type of PEP 8 naming convention
def is_name_conformant(name, name_type):
    pattern = pep8_naming_conventions.get(name_type)
    if not pattern:
        raise ValueError(f"Invalid name type: {name_type}")
    if not re.match(pattern, name):
        return False
    # Special case for function names, variable names, and constant names: check if the name is a compound word
    if name_type in ["function", "variable", "constant"]:
        parts = name.split('_')
        for part in parts:
            if len(split_compound_word(part)) > 1:
                return False
    return True



# Define a set of unit tests to check the correctness of the is_name_conformant function
class TestPep8Conventions(unittest.TestCase):
    # Test cases for class names
    def test_class_name(self):
        self.assertTrue(is_name_conformant("MyClass", "class"))
        self.assertFalse(is_name_conformant("my_class", "class"))
        self.assertFalse(is_name_conformant("myclass", "class"))
        self.assertFalse(is_name_conformant("My_Class", "class"))
        self.assertFalse(is_name_conformant("myClass", "class"))

    # Test cases for function names
    def test_function_name(self):
        self.assertTrue(is_name_conformant("my_function", "function"))
        self.assertFalse(is_name_conformant("myFunction", "function"))
        self.assertFalse(is_name_conformant("MyFunction", "function"))
        self.assertFalse(is_name_conformant("my-function", "function"))
        self.assertFalse(is_name_conformant("myfunction", "function"))
        self.assertFalse((is_name_conformant("my_functiontwo", "function")))

    # Test cases for variable names
    def test_variable_name(self):
        self.assertTrue(is_name_conformant("my_variable", "variable"))
        self.assertFalse(is_name_conformant("myVariable", "variable"))
        self.assertFalse(is_name_conformant("MyVariable", "variable"))
        self.assertFalse(is_name_conformant("my-variable", "variable"))
        self.assertFalse(is_name_conformant("myvariable", "variable"))

    # Test cases for constant names
    def test_constant_name(self):
        self.assertTrue(is_name_conformant("MY_CONSTANT", "constant"))
        self.assertFalse(is_name_conformant("my_constant", "constant"))
        self.assertFalse(is_name_conformant("MyConstant", "constant"))
        self.assertFalse(is_name_conformant("MY-CONSTANT", "constant"))
        self.assertFalse(is_name_conformant("MYCONSTANT", "constant"))


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
