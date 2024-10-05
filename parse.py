import argparse
from enum import Enum


class ProblemType(Enum):
    LEETCODE = 'leetcode'
    ROSALIND = 'rosalind'
    HACKERRANK = 'hackerrank'


class ProgrammingLanguage(Enum):
    CPP = ('cpp', 'C++')
    JAVA = ('java', 'Java')
    PYTHON = ('python', 'Python')
    C = ('c', 'C')
    CSHARP = ('csharp', 'C#')
    JAVASCRIPT = ('javascript', 'JavaScript')
    TYPESCRIPT = ('typescript', 'TypeScript')
    PHP = ('php', 'PHP')
    SWIFT = ('swift', 'Swift')
    KOTLIN = ('kotlin', 'Kotlin')
    DART = ('dart', 'Dart')
    GO = ('go', 'Go')
    RUBY = ('ruby', 'Ruby')
    SCALA = ('scala', 'Scala')
    RUST = ('rust', 'Rust')
    RACKET = ('racket', 'Racket')
    ERLANG = ('erlang', 'Erlang')
    ELIXIR = ('elixir', 'Elixir')

    def __init__(self, arg_name, output_name):
        self.arg_name = arg_name
        self.output_name = output_name


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse command line arguments for problem solving.")

    parser.add_argument('--problem-file', type=str, required=True, help="Path to the problem file")

    problem_type_group = parser.add_mutually_exclusive_group(required=True)
    problem_type_group.add_argument('-l', '--leetcode', action='store_const', const=ProblemType.LEETCODE,
                                    dest='problem_type')
    problem_type_group.add_argument('-r', '--rosalind', action='store_const', const=ProblemType.ROSALIND,
                                    dest='problem_type')
    problem_type_group.add_argument('-k', '--hackerrank', action='store_const', const=ProblemType.HACKERRANK,
                                    dest='problem_type')

    lang_group = parser.add_mutually_exclusive_group(required=True)
    for lang in ProgrammingLanguage:
        lang_group.add_argument(f'--{lang.arg_name}',
                                action='store_const', const=lang, dest='programming_language')

    args = parser.parse_args()

    return args.problem_type, args.problem_file, args.programming_language
