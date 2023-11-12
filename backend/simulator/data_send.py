import os
import time
from datetime import datetime

import requests

import file_processing
from bootstrap import bootstrap
from file_processing import DATE_COLUMN, DATE_FORMAT, READ_FILE_PATH
from database.Repository import Repository
from models.Destination import Destination
from simulator.data_characteristics import *

WAIT_TIME_LONG = 1
WAIT_TIME_SHORT = 0.2

SEND_API_PATH = 'http://127.0.0.1:5000/api/stations/'
ADD_DEST_API_PATH = 'http://127.0.0.1:5000/api/add_dest'


def infinity_send_data():

    bootstrap()
    r = Repository(
        os.getenv('DATABASE_URL'),
        os.getenv('DATABASE_PASSWORD')
   )

    # if
    # order bu date, take last element
    current_row_index = 0

    data = file_processing.read_data(READ_FILE_PATH)
    data = convert_int64_to_int(data)
    data_length = get_data_length(data)

    start_date = None
    start_time = datetime.now()
    # skip date
    date_difference = None

    is_waiting = False

    while current_row_index < data_length:

        # if not is_waiting:
        date_string = data[DATE_COLUMN][current_row_index]
        date = datetime.strptime(date_string, DATE_FORMAT)
        if start_date is None:
            start_date = date
        date_difference = date - start_date
        start_date = date
            # TODO: Connection with DB

        current_time = datetime.now()

        time_difference = current_time - start_time
        print(f'{time_difference} of {date_difference}')

        # is_requested = time_difference >= date_difference

        # if is_requested:
        # todo: добавить прооверку на правильность отправки запроса
        destination = dict(data.loc[current_row_index])
        json = {
                'destination': destination,
            }
        requests.post(ADD_DEST_API_PATH, json=json)
        current_row_index += 1
        start_time = datetime.now()
        # is_waiting = False
        # else:
            # is_waiting = True

        """if is_waiting:
            time.sleep(WAIT_TIME_LONG)
        else:
            time.sleep(WAIT_TIME_SHORT)"""
        time.sleep(1)


infinity_send_data()
