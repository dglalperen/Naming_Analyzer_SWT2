

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