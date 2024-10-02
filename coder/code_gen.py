from coder import (
    STARTING_A_NEW_PROBLEM_PROMPT,
    SUBMITTING_A_CODE_ERROR_PROMPT,
    CODE_EXAMPLE_PREFIX,
    ADVOCATE_FOR_BETTER_SOLUTION_ON_RETRY,
    END_OF_PROMPT_INSTRUCTIONS_FOR_CLEAR_RESPONSE
)


class CodeGenerationAndErrorHandling:
    def __init__(self, claude_api):
        self.claude_api = claude_api

    def generate_code(self, problem_description, starting_code):
        prompt = f"{STARTING_A_NEW_PROBLEM_PROMPT}\n\n{problem_description}\n\n{CODE_EXAMPLE_PREFIX}\n{starting_code}"
        return self.claude_api.send_prompt(prompt)

    def handle_error(self, problem_description, current_code, starting_code, error_message, error_info):
        prompt = f"""{SUBMITTING_A_CODE_ERROR_PROMPT}

{problem_description}

{ADVOCATE_FOR_BETTER_SOLUTION_ON_RETRY}
{current_code}

Error Message:
{error_message}

Detailed Error Information:
{error_info}

{CODE_EXAMPLE_PREFIX}
{starting_code}

{END_OF_PROMPT_INSTRUCTIONS_FOR_CLEAR_RESPONSE}"""
        return self.claude_api.send_prompt(prompt)
