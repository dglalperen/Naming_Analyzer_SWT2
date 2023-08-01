prompt = """Title: Advanced Python Source Code Naming Analysis
    Prompt:
    As a highly trained AI model developed by OpenAI, your task is to conduct an in-depth analysis of the naming conventions used in a given Python source code. The aim is to evaluate the quality, appropriateness, and consistency of the names used for functions (excluding `__init__` and other dunder methods), classes, and variables (excluding loop iterators like `i` and `j`).

    In this analysis, consider the following criteria:
    - **Descriptiveness**: The names should be descriptive and relevant to their associated code. For example, a function meant to calculate an average could be named 'calculate_average', while 'calc_avg' might be somewhat less clear, and 'function1' would be vague and misleading.
    - **Length**: Very short names (like 'a' or 'x') may not provide enough information about what they represent, while very long names can be cumbersome and may be a sign of trying to do too much with a single variable or function.
    - **Common Misuses**: Names consisting of generic terms (like 'data', 'value') or Python reserved words should be avoided unless their usage is universally understood in the context of programming.
    - **Consistency**: Check for consistency in naming conventions across the codebase. A name might be semantically correct in isolation but if it's not consistent with the rest of the codebase, it can be confusing for others reading the code.
    - **Domain-Specific Conventions**: Depending on the purpose of the program, there may be specific naming conventions or practices that should be followed.

    Your analysis results should be formatted as a JSON object, following this schema:
    {
        "score": "<score>"
    }
    Here, `<score>` represents the calculated score between 0 and 1, expressed as a decimal number in string format. This score should reflect the overall quality of naming in the codebase, taking into account the factors mentioned above. It is the value of the "score" key in the provided JSON schema.
    """
