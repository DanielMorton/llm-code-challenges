from coder.code_gen import CodeGeneration
from coder.leetcoder import LeetCoder
from credentials import get_credentials


def run(df, programming_language):
    df = df[df['Language'] == programming_language]
    code_gen = CodeGeneration("")
    coder = LeetCoder(code_gen, programming_language, headless=False)

    username, password = get_credentials()
    coder.login(username, password)
    problem_title = coder.problem_navigator.navigate_to_new_problem(df)
    coder.complete_individual_problem(problem_title)
