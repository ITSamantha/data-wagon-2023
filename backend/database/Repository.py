import datetime
import json

from database.Dao import Dao
from models.Destination import DestinationTrainResponse
from utils import FileParser, ModelConverter


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
        stations, roads_dicts = self.__dao.selectStationsByRadiusWithRoads(
            longitude=longitude,
            latitude=latitude,
            radius=radius
        )

        stations_dicts = list()
        for station_model in stations:
            stations_dicts.append(
                ModelConverter.stationToDict(station_model)
            )

        roads_dicts = list()
        for roads_model in roads_dicts:
            roads_dicts.append(
                ModelConverter.roadToDict(roads_model)
            )

        json_data = {
            'stations': stations_dicts,
            'network': roads_dicts
        }

        return json.dumps(json_data, indent=2)

    def getAllRoads(self):
        return self.__dao.getAllRoads()

    def addDestination(self, destination):
        self.__dao.insertDestination(destination)

    def getDateTimeForPeople(self, d: datetime.datetime):
        return d.strftime('%d.%m.%Y %H:%M:%S')

    def makeTimeRangeForDest(self, destinations: list):
        count_dests = len(destinations)
        if count_dests == 0:
            return destinations

        newDestinations = list()
        timeFrom = destinations[0].oper_date
        curr_st_id = destinations[0].st_id

        for i in range(1, count_dests):
            dest = destinations[i]
            if (curr_st_id != dest.st_id):
                timeRange = self.getDateTimeForPeople(timeFrom) + ' - ' + self.getDateTimeForPeople(dest.oper_date)
                newDestinations.append(
                    DestinationTrainResponse(
                        timeRange,
                        curr_st_id
                    )
                )
                curr_st_id = dest.st_id
                timeFrom = dest.oper_date
                if count_dests - 1 == i:
                    newDestinations.append(
                        DestinationTrainResponse(
                            self.getDateTimeForPeople(timeFrom),
                            curr_st_id
                        )
                    )
            else:
                if count_dests - 1 == i:
                    timeRange = self.getDateTimeForPeople(timeFrom) + ' - ' + self.getDateTimeForPeople(dest.oper_date)
                    newDestinations.append(
                        DestinationTrainResponse(
                            timeRange,
                            curr_st_id
                        )
                    )

        return newDestinations

    def getDestinationsByTrainId(self, train_id):
        destinations = self.__dao.getDestinationsByTrainId(train_id=train_id)
        destinations = self.makeTimeRangeForDest(destinations)
        dest_dicts = list()
        for destination in destinations:
            dest_dicts.append(
                ModelConverter.trainDestinationResponseToDict(destination)
            )
        return json.dumps(dest_dicts, indent=2)

    def getActualDestinations(self):
        destinations = self.__dao.getActualDestinations()
        dest_dicts = list()
        for destination in destinations:
            dest_dicts.append(
                ModelConverter.actualDestToDict(destination)
            )
        return json.dumps(dest_dicts, indent=2)

    def getActualWagons(self, train_id):
        destinations = self.__dao.getActualWagons(train_id)
        dest_ids = list()
        for destination in destinations:
            dest_ids.append(destination.wag_id)

        if len(destinations) > 0:
            dest_dict = ModelConverter.actualTrainWagonsToDict(
                train_id,
                destinations[0].st_id,
                longitude=destinations[0].longitude,
                latitude=destinations[0].latitude,
                wagons=dest_ids
            )
            return json.dumps(dest_dict, indent=2)
        return json.dumps({}, indent=2)

    def parseDestinations(self, file_name):
        destinations = FileParser.getDestinations(file_name)
        for destination in destinations:
            self.addDestination(destination)