from backend.models.Destination import DestinationTrain, DestinationTrainResponse
from backend.models.Road import Road
from backend.models.Station import Station


def roadToDict(road: Road):
    return {
        "from": road.start_id,
        "to": road.end_id,
        "dist": road.len
    }


def stationToDict(station: Station):
    return {
        "longitude": station.longitude,
        "latitude": station.latitude,
        "id": station.st_id
    }


def trainDestinationToDict(dest: DestinationTrain):
    return {
        "station": dest.st_id,
        "time": dest.oper_date
    }


def trainDestinationResponseToDict(dest: DestinationTrainResponse):
    return {
        "station": dest.st_id,
        "time": dest.oper_date
    }
