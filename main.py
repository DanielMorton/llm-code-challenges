from parse import parse_arguments
from read import read_or_create_dataframe


def main():
    try:
        problem_type, problem_file, programming_language = parse_arguments()
        print(f"Problem type: {problem_type}")
        print(f"Problem file: {problem_file}")
        print(f"Programming language: {programming_language.value}")

        df = read_or_create_dataframe(problem_file)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
