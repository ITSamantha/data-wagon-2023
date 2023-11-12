import pandas as pd


def get_data_length(data):
    return len(data)


def convert_int64_to_int(data):
    modified_data = data.copy()

    for column in modified_data.columns:
        if pd.api.types.is_int64_dtype(modified_data[column]):
            modified_data[column] = modified_data[column].astype(str)

    return modified_data