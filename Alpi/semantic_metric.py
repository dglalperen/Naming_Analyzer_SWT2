from semantic_evaluation import request_code_improvement,ask_chatgpt


good_example = "./prompt_test_good_example.py"
moderate_example = "./prompt_test_moderate_example.py"
bad_example = "./prompt_test_bad_example.py"
print(ask_chatgpt(bad_example))