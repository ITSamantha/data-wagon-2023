import time
from datetime import datetime
import requests
import file_processing

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
WAIT_TIME_LONG = 1
WAIT_TIME_SHORT = 0.2
READ_FILE_PATH = 'reversed_output.csv'


def infinity_send_data():
    current_row_index = 0

    data = file_processing.read_data(READ_FILE_PATH)
    data_length = get_data_length(data)

    start_date = None
    start_time = datetime.now()

    date_difference = None

    is_waiting = False

    while current_row_index < data_length:

        if not is_waiting:
            date_string = data['OPERDATE'][current_row_index]
            date = datetime.strptime(date_string, DATE_FORMAT)
            print(date)
            if start_date is None:
                start_date = date
            date_difference = date - start_date
            start_date = date
            # TODO: Connection with DB

        current_time = datetime.now()

        time_difference = current_time - start_time
        print(f'{time_difference} of {date_difference}')

        is_requested = time_difference >= date_difference

        if is_requested:
            r = requests.get('http://127.0.0.1:5000/api/stations/')
            print(r.json())
            print()
            current_row_index += 1
            start_time = datetime.now()
            is_waiting = False
        else:
            is_waiting = True

        if is_waiting:
            time.sleep(WAIT_TIME_LONG)
        else:
            time.sleep(WAIT_TIME_SHORT)


def get_data_length(data):
    return len(data)


infinity_send_data()
