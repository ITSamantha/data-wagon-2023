import json

from backend.database.Dao import Dao
from backend.models.Road import Road
from backend.utils import FileParser, ModelConverter


class Repository:
    def __init__(self, config, password):
        self.__dao = Dao(config, password)

    def __loadRoadsFromFileToDb(self, dir_name):
        stations = self.__dao.selectStations()
        roads = FileParser.getRoads(dir_name)
        correct_roads = list()
        for road in roads:
            if road.end_id  in stations and road.start_id in stations:
                correct_roads.append(road)

        self.__dao.insertRoads(correct_roads)

    def __loadStationsFromFileToDb(self, dir_name):
        stations = FileParser.getStations(dir_name)
        self.__dao.insertStations(stations)

    def parseFromFileToDb(self, dir_name):
        self.__dao.deleteAllRoads()
        self.__dao.deleteAllStations()
        self.__loadStationsFromFileToDb(dir_name)
        self.__loadRoadsFromFileToDb(dir_name)

    def __getRoads(self, start_st_id):
        road_models = self.__dao.selectRoads(start_st_id,)
        return road_models
        # road_dicts = list()
        # for roadModel in road_models:
        #     road_dicts.append(
        #         ModelConverter.roadToDict(roadModel)
        #     )
        # return json.dumps(road_dicts, indent=2)

    def getStationsJson(
            self,
            longitude,
            latitude,
            radius
    ):
        stations = self.__dao.selectStationsByRadius(
            longitude=longitude,
            latitude=latitude,
            radius=radius
        )

        all_roads = list()
        all_stations = list()
        all_stations += stations

        for station in stations:

            roads = self.__getRoads(station.st_id)
            all_roads += roads
            for road in roads:
                if road.end_id not in all_stations:
                    all_stations.append(self.__dao.selectStationsById(road.end_id))

        stations_dicts = list()

        for station_model in all_stations:
            stations_dicts.append(
                ModelConverter.stationToDict(station_model)
            )

        roads_dicts = list()
        for roads_model in all_roads:
            roads_dicts.append(
                ModelConverter.roadToDict(roads_model)
            )

        json_data = {
            'stations': stations_dicts,
            'network': roads_dicts
        }

        return json.dumps(json_data, indent=2)
