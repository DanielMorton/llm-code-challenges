import argparse
from enum import Enum


class ProblemType(Enum):
    LEETCODE = 'leetcode'
    ROSALIND = 'rosalind'
    HACKERRANK = 'hackerrank'


class ProgrammingLanguage(Enum):
    CPP = 'cpp'
    JAVA = 'java'
    PYTHON = 'python'
    C = 'c'
    CSHARP = 'csharp'
    JAVASCRIPT = 'javascript'
    TYPESCRIPT = 'typescript'
    PHP = 'php'
    SWIFT = 'swift'
    KOTLIN = 'kotlin'
    DART = 'dart'
    GO = 'go'
    RUBY = 'ruby'
    SCALA = 'scala'
    RUST = 'rust'
    RACKET = 'racket'
    ERLANG = 'erlang'
    ELIXIR = 'elixir'


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
        lang_group.add_argument(f'--{lang.name.lower()}',
                                action='store_const', const=lang, dest='programming_language')

    args = parser.parse_args()

    return args.problem_type, args.problem_file, args.programming_language
