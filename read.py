import pandas as pd


def read_or_create_dataframe(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            print(f"File '{file_path}' read successfully.")
            return df
        except pd.errors.EmptyDataError:
            print(f"File '{file_path}' is empty. Creating a new DataFrame.")
    else:
        print(f"File '{file_path}' not found. Creating a new DataFrame.")

    return pd.DataFrame(columns=["Problem Name", "Language", "Result"])