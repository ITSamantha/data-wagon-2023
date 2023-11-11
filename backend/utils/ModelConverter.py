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
