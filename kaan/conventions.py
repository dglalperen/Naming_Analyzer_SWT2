import re
import nltk
import unittest
from nltk.corpus import words

nltk.download('words')

# Create a set of English words
english_words = set(words.words())

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

pep8_naming_conventions = {
    "function": r"^[a-z_][a-z0-9_]{2,30}$",
    "class": r"^[A-Z][a-zA-Z0-9]{2,30}$",
    "variable": r"^[a-z_][a-z0-9_]{2,30}$",
    "constant": r"^[A-Z_][A-Z0-9_]{2,30}$",
}



def is_name_conformant(name, name_type):
    pattern = pep8_naming_conventions.get(name_type)
    if not pattern:
        raise ValueError(f"Invalid name type: {name_type}")
    if not re.match(pattern, name):
        return False
    # Special case for function names, variable names, and constant names: check if the name is a compound word
    if name_type in ["function_name", "variable_name", "constant_name"] and "_" not in name:
        return len(split_compound_word(name)) <= 1
    return True


class TestPep8Conventions(unittest.TestCase):

    def test_module_name(self):
        self.assertTrue(is_name_conformant("my_module", "module_name"))
        self.assertFalse(is_name_conformant("MyModule", "module_name"))
        self.assertFalse(is_name_conformant("myModule", "module_name"))
        self.assertFalse(is_name_conformant("my-module", "module_name"))

    def test_class_name(self):
        self.assertTrue(is_name_conformant("MyClass", "class_name"))
        self.assertFalse(is_name_conformant("my_class", "class_name"))
        self.assertFalse(is_name_conformant("myclass", "class_name"))
        self.assertFalse(is_name_conformant("My_Class", "class_name"))
        self.assertFalse(is_name_conformant("myClass", "class_name"))

    def test_function_name(self):
        self.assertTrue(is_name_conformant("my_function", "function_name"))
        self.assertFalse(is_name_conformant("myFunction", "function_name"))
        self.assertFalse(is_name_conformant("MyFunction", "function_name"))
        self.assertFalse(is_name_conformant("my-function", "function_name"))
        self.assertFalse(is_name_conformant("myfunction", "function_name"))

    def test_variable_name(self):
        self.assertTrue(is_name_conformant("my_variable", "variable_name"))
        self.assertFalse(is_name_conformant("myVariable", "variable_name"))
        self.assertFalse(is_name_conformant("MyVariable", "variable_name"))
        self.assertFalse(is_name_conformant("my-variable", "variable_name"))
        self.assertFalse(is_name_conformant("myvariable", "variable_name"))

    def test_constant_name(self):
        self.assertTrue(is_name_conformant("MY_CONSTANT", "constant_name"))
        self.assertFalse(is_name_conformant("my_constant", "constant_name"))
        self.assertFalse(is_name_conformant("MyConstant", "constant_name"))
        self.assertFalse(is_name_conformant("MY-CONSTANT", "constant_name"))
        self.assertFalse(is_name_conformant("MYCONSTANT", "constant_name"))


    # Add more tests for other name types...

if __name__ == "__main__":
    unittest.main()
