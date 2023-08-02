import unittest

from Alpi.semantic_evaluation import ask_chatgpt


class TestChatGPTFunctions(unittest.TestCase):
    def setUp(self):
        # Here you should define the path to a Python file that will be used for testing.
        # Make sure this file exists and contains valid Python code.
        self.example_file_path = "prompt_test_bad_example.py"

    def test_ask_chatgpt(self):
        # Mock OpenAI ChatCompletion.create response
        class MockResponse:
            def __init__(self):
                self.data = {'choices': [{'message': {'content': '{"score": "0.6"}'}}]}

            # Add this method to make MockResponse subscriptable
            def __getitem__(self, key):
                return self.data[key]

        def mock_create(*args, **kwargs):
            return MockResponse()

        # Call the function with the test file
        result = ask_chatgpt(self.example_file_path)

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the dictionary has a "score" key
        self.assertIn("score", result)

        # Check that the score is a string
        self.assertIsInstance(result["score"], str)

        # Check that the score string can be converted to a float between 0 and 1
        score_value = float(result["score"])
        self.assertGreaterEqual(score_value, 0.0)
        self.assertLessEqual(score_value, 1.0)


if __name__ == '__main__':
    unittest.main()
