import run_hackerrank
import run_leetcode
import run_rosalind
from parse import parse_arguments, ProblemType
from read import read_or_create_dataframe


def main():
    try:
        problem_type, problem_file, programming_language = parse_arguments()
        print(f"Problem type: {problem_type}")
        print(f"Problem file: {problem_file}")
        print(f"Programming language: {programming_language}")

        df = read_or_create_dataframe(problem_file)
        if problem_type == ProblemType.LEETCODE:
            run_leetcode.run(df, programming_language)
        elif problem_type == ProblemType.HACKERRANK:
            run_hackerrank.run(df, programming_language)
        elif problem_type == ProblemType.ROSALIND:
            run_rosalind.run(df, programming_language)
        else:
            raise ValueError(f"Unexpected problem type: {problem_type}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
