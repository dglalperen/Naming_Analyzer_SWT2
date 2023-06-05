prompt = """As an AI language model, your assignment is to conduct an in-depth analysis of Python source code.
            You're tasked with evaluating the appropriateness of function (excluding __init__ functions),
            class, and variable names based on how clearly and accurately they convey their semantic roles in the code.
            For instance, in the case of a function that calculates an average,
            a name like calculate_average would be considered clear and accurate, while a name like calc_avg might be seen as less clear,
            and a name like function1 would be considered unclear and inaccurate.
            Single-letter names or names that are common words (like x, y, f, A, e) are considered non-descriptive
            unless their purpose is universally understood in the context of programming (such as i for an iteration variable in a loop).
            Ignore __init__ functions in your analysis, as their naming is governed by Python's object-oriented programming conventions
            and cannot be incorrect.
            Your analysis should compute a score on a scale from 0 to 1, based on the following criteria:
            Descriptiveness (50% weightage): Do the names adequately describe the purpose of the function, class,
            or variable? Names that are too generic, ambiguous or do not clearly indicate their purpose should be considered non-descriptive.
            Brevity (16.7% weightage): Are the names concise without sacrificing clarity? Names that are unnecessarily long and complex,
            or too brief to be clear should be penalized.
            Consistency (16.7% weightage): Do the names follow a consistent pattern throughout the code? Inconsistent naming patterns can confuse readers and should be avoided.
            Conformity (16.6% weightage): Do the names adhere to Python's naming conventions (PEP 8)? Names that violate these conventions should be penalized.
            A score of 1 signifies complete alignment between the names and their semantic roles, and full adherence to the criteria above.
            The results of your analysis must be provided in a JSON format, adhering to the following schema:

            {
                "score": "<score>"
            }
            Where <score> is the calculated score between 0 and 1. Note that the score must be a decimal number represented as a string in the JSON. The score must be presented solely as the value of the "score" key in the provided JSON schema."""
