import pandas as pd


def write_csv():
    input_file_path = 'disl_hackaton.xlsx'
    output_file_path = 'reversed_output.csv'

    df = pd.read_excel(input_file_path)

    df_sorted = df.sort_values(by='OPERDATE')

    df_sorted.to_csv(output_file_path, index=False)

    print(f"Sorted and Reversed Excel file written to {output_file_path}")


def read_data(path):
    data = pd.read_csv(path)
    return data

