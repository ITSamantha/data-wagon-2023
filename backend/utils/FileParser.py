from datetime import datetime

import pandas as pd

from database.Dao import Dao
from models.Destination import Destination
from models.Road import Road
from models.Station import Station


def getRoads(dir_name):
    file_name = dir_name + roads_file_name
    roads = list()
    reader = pd.ExcelFile(file_name)

    sheet = reader.parse("Sheet 1")
    for row in sheet.iloc:
        roads.append(__getRoadFromLine(row))
    return roads


def __getRoadFromLine(line):
    return Road(
        int(line.iloc[0]),
        int(line.iloc[1]),
        int(line.iloc[2]),
        0
    )


def __getStationFromLine(line):
    return Station(
        int(line.iloc[0]),
        float(line.iloc[1]),
        float(line.iloc[2])
    )


def getStations(dir_name):
    file_name = dir_name + stations_file_name
    stations = list()
    reader = pd.ExcelFile(file_name)

    sheet = reader.parse("Sheet 1")
    for row in sheet.iloc:
        stations.append(__getStationFromLine(row))
    return stations


def __getDestinationsFromLine(line):
    # date = datetime.strptime(
    #     line.iloc[1],
    #     "%d.%m.%Y %h:%m:%s"
    # )

    date = datetime.fromtimestamp(line[1])
    train_info = line.iloc[4].strip('-')
    train_id = train_info[0]
    form_st_id = train_info[1]
    target_st_id = train_info[2]

    return Destination(
        int(line.iloc[0]),
        date,
        int(line.iloc[2]),
        int(line.iloc[3]),
        int(train_id),
        int(0),
        int(form_st_id),
        int(target_st_id)
    )


def getDestinations(dir_name):
    file_name = dir_name + dest_file_name
    destinations = list()
    reader = pd.ExcelFile(file_name)
    for sheet_name in reader.sheet_names:
        sheet = reader.parse(sheet_name)
        for row in sheet.iloc:
            destinations.append(__getDestinationsFromLine(row))
    return destinations


stations_file_name = 'STATION_COORDS_HACKATON.xlsx'
roads_file_name = 'PEREGON_HACKATON.xlsx'
dest_file_name = 'disl_hackaton.xlsx'
