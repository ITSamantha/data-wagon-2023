import pandas as pd

DATE_COLUMN = 'OPERDATE'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

READ_FILE_PATH = '/home/artem/data-wagon/backend/simulator/reversed_output.csv'


def write_csv(input_file):
    try:
        output_file_path = f"{input_file.split('.')[0]}.csv "
        df = pd.read_excel(input)
        df_sorted = df.sort_values(by=DATE_COLUMN)
        df_sorted.to_csv(output_file_path, index=False)
        return True

    except Exception as e:
        print(f'Exception occured: {e}')
        return False


def write_csv_data(input_file):
    try:
        output_file_path = f"{input_file.split('.')[0]}.csv "
        df = pd.read_excel(input_file)
        df.to_csv(output_file_path, index=False)
        return True

    except Exception as e:
        print(f'Exception occured: {e}')
        return False


def read_data(path):
    try:
        data = pd.read_csv(path)
        return data

    except Exception as e:
        print(f'Exception occured: {e}')
        return None