ADVOCATE_FOR_BETTER_SOLUTION_ON_RETRY = "Don't use the same approach as the current code which looks like this, review what part of the description we're likely not meeting the requirements of and make a new solution with an approach that likely is a better fix."  # Prompt for Claude to suggest a better solution on retry
CODE_EXAMPLE_PREFIX = "Here's the starting code provided by LeetCode:"  # Prefix for introducing LeetCode's starting code to Claude
END_OF_PROMPT_INSTRUCTIONS_FOR_CLEAR_RESPONSE = "Provide only the Python code solution, with no additional text, comments, or questions before or after the code. The solution must start with the same class solution object and function definition(s) and their parameter(s) that the starting code had."  # Instructions for Claude to provide a clear response


INNER_HTML = 'innerHTML'

PROBLEM_DESCRIPTION = 'div[data-track-load="description_content"]'

RUN_BUTTON = 'button[data-e2e-locator="console-run-button"]'

RUNTIME_ERROR = "//div[contains(@class, 'bg-fill-4')]/div/div[contains(@class, 'font-menlo')]"

SUBMIT_BUTTON = 'button[data-e2e-locator="console-submit-button"]'

STARTING_A_NEW_PROBLEM_PROMPT = "Solve this LeetCode problem in Python, optimizing for the fastest runtime approach with the best time complexity unless there is a required time complexity in the description, in that case your solution must match that time complexity. Provide only the Python code solution, with no additional text, comments, or questions before or after the code:"  # Prompt for Claude when starting a new problem
SUBMITTING_A_CODE_ERROR_PROMPT = "We need to fix our code for a leetcode python problem. Here's what the problem description was: "  # Prompt for Claude when submitting a code with errors

TEST_CASE_BUTTON = 'div.cursor-pointer.rounded-lg.px-4.py-1.font-medium'
TEST_CASE_INPUTS =  "//div[contains(@class, 'bg-fill-4')]/div/div[contains(@class, 'font-menlo')]"
TEST_CASE_OUTPUTS = 'div.flex.h-full.w-full.flex-col.space-y-2'