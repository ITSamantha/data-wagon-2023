from backend.models.Destination import DestinationTrain, DestinationTrainResponse, ActualDestination, ActualWagon
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


def actualDestToDict(dest: ActualDestination):
    return {
        "train_id": dest.train_id,
        "st_id": dest.st_id,
        "longitude": dest.longitude,
        "latitude": dest.latitude
    }


def actualWagonToDict(dest: ActualWagon):
    return {
        "wag_id": dest.wag_id,
        "st_id": dest.st_id,
        "longitude": dest.longitude,
        "latitude": dest.latitude
    }


def actualTrainWagonsToDict(
        train_id: int,
        st_id: int,
        longitude: float,
        latitude: float,
        wagons: list
):
    return {
        "train_id": train_id,
        "st_id": st_id,
        "longitude": longitude,
        "latitude": latitude,
        "wagons": wagons
    }
