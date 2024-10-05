from coder.leetcoder import LeetCoder
from credentials import get_credentials


def run(df, programming_language):
    df = df[df['Language'] == programming_language]
    username, password = get_credentials()
    coder = LeetCoder()
    coder.login(username, password)
    coder.navigate_to_new_problem(df)
