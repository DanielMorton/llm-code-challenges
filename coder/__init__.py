CODE_EXAMPLE_PREFIX = "Starting code:"  # Prefix for introducing LeetCode's starting code to Claude
CODE_ONLY = "Provide only the code solution, with no additional text, comments, or questions before or after the code. The solution must start with the same class solution object and function definition(s) and their parameter(s) that the starting code had."  # Instructions for Claude to provide a clear response

LEETCODEFILTER = 'https://leetcode.com/problemset/?page='
LEETCODE_PROBLEM_PREFIX = "https://leetcode.com/problems/"

INNER_HTML = 'innerHTML'

PROBLEM_DESCRIPTION = 'div[data-track-load="description_content"]'

RUN_BUTTON = 'button[data-e2e-locator="console-run-button"]'

RUNTIME_ERROR = "//div[contains(@class, 'bg-fill-4')]/div/div[contains(@class, 'font-menlo')]"

SUBMIT_BUTTON = 'button[data-e2e-locator="console-submit-button"]'

STARTING_A_NEW_PROBLEM_PROMPT = "Solve this LeetCode problem:"  # Prompt for Claude when starting a new problem
SUBMITTING_A_CODE_ERROR_PROMPT = "Solution Failed:"  # Prompt for Claude when submitting a code with errors

TEST_CASE_BUTTON = 'div.cursor-pointer.rounded-lg.px-4.py-1.font-medium'
TEST_CASE_INPUTS = "//div[contains(@class, 'bg-fill-4')]/div/div[contains(@class, 'font-menlo')]"
TEST_CASE_OUTPUTS = 'div.flex.h-full.w-full.flex-col.space-y-2'
