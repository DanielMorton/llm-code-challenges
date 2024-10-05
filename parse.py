import argparse
from enum import Enum


class ProblemType(Enum):
    LEETCODE = 'leetcode'
    ROSALIND = 'rosalind'
    HACKERRANK = 'hackerrank'


class ProgrammingLanguage(Enum):
    CPP = 'C++'
    JAVA = 'Java'
    PYTHON = 'Python'
    C = 'C'
    CSHARP = 'C#'
    JAVASCRIPT = 'Javascript'
    TYPESCRIPT = 'Typescript'
    PHP = 'PHP'
    SWIFT = 'Swift'
    KOTLIN = 'Kotlin'
    DART = 'Dart'
    GO = 'Go'
    RUBY = 'Ruby'
    SCALA = 'Scala'
    RUST = 'Rust'
    RACKET = 'Racket'
    ERLANG = 'Erlang'
    ELIXIR = 'Elixir'


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse command line arguments for problem solving.")

    parser.add_argument('--problem-file', type=str, required=True, help="Path to the problem file")

    problem_type_group = parser.add_mutually_exclusive_group(required=True)
    for prob_type in ProblemType:
        problem_type_group.add_argument(f'-{prob_type.name[0].lower()}', f'--{prob_type.value}',
                                        action='store_const', const=prob_type, dest='problem_type')

    lang_group = parser.add_mutually_exclusive_group(required=True)
    for lang in ProgrammingLanguage:
        lang_group.add_argument(f'--{lang.name.lower()}',
                                action='store_const', const=lang, dest='programming_language')

    args = parser.parse_args()

    return args.problem_type, args.problem_file, args.programming_language
