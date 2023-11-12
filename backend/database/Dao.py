import psycopg2

from database import DatabaseScripts
from models.Destination import Destination, DestinationTrain, ActualWagon, ActualDestination
from models.Road import Road
from models.Station import Station


class Dao:

    def __init__(self, config, password):
        self.__conn = None
        self.__config = config.format(password)

    def __connect(self):
        try:
            self.__conn = psycopg2.connect(self.__config)
            return self.__conn.cursor()
        except:
            print('Connect to DB - ERROR !')

    def __insertOneDestination(self, cursor, destination: Destination):
        try:
            cursor.execute(
                DatabaseScripts.insertDestQuery,
                (
                    destination.wag_id,
                    destination.oper_date,
                    destination.disl_st_id,
                    destination.dest_st_id,
                    destination.train_id,
                    destination.form_st_id,
                    destination.target_st_id,
                )
            )
        except:
            pass

    def __insertOneStation(self, cursor, station: Station):
        cursor.execute(
            DatabaseScripts.insertStationsQuery,
            (
                station.st_id, station.latitude, station.longitude
            )
        )

    def deleteAllStations(self):
        curs = self.__connect()
        curs.execute(
            DatabaseScripts.deleteStationsQuery
        )
        self.__disconnect(curs)

    def deleteAllRoads(self):
        curs = self.__connect()
        curs.execute(
            DatabaseScripts.deleteRoadsQuery
        )
        self.__disconnect(curs)

    def getAllRoads(self):
        cursor = self.__connect()
        cursor.execute(
            DatabaseScripts.selectAllRoadsWithCities,
        )
        row = cursor.fetchall()
        return row

    def insertStations(self, stations: list):
        curs = self.__connect()
        for station in stations:
            self.__insertOneStation(curs, station)
        self.__disconnect(curs)

    def insertStation(self, station: Station):
        curs = self.__connect()
        self.__insertOneStation(curs, station)
        self.__disconnect(curs)

    def __insertOneRoad(self, cursor, road: Road):
        try:
            cursor.execute(
                DatabaseScripts.insertRoadQuery,
                (
                    road.start_id,
                    road.end_id,
                    road.len
                )
            )
        except Exception as e:
            # IGNORE MISSING STATIONS
            print(e)

    def insertRoad(self, road: Road):
        cursor = self.__connect()
        self.__insertOneRoad(cursor, road)
        self.__disconnect(cursor)

    def insertRoads(self, roads: list):
        cursor = self.__connect()
        for road in roads:
            self.__insertOneRoad(cursor, road)
        self.__disconnect(cursor)

    def selectRoads(self, start_st_id):
        roads = list()
        cursor = self.__connect()
        cursor.execute(
            DatabaseScripts.selectRoadsByStartStationQuery,
            (
                start_st_id,
            )
        )
        rows = cursor.fetchall()
        for row in rows:
            road = Road(
                row[0],
                row[1],
                row[2],
                0
            )
            roads.append(road)
        self.__disconnect(cursor)
        return roads

    def selectStations(
            self
    ):
        stations = list()
        cursor = self.__connect()
        cursor.execute(
            DatabaseScripts.selectAllStationsQuery
        )
        rows = cursor.fetchall()
        for row in rows:
            station = Station(
                row[0],
                row[1],
                row[2]
            )
            stations.append(station)
        self.__disconnect(cursor)
        return stations

    def selectStationsByRadiusWithRoads(
            self,
            radius,
            longitude,
            latitude
    ):
        cursor = self.__connect()
        cursor.execute(
            DatabaseScripts.selectStationsByRadiusQuery,
            (
                longitude, radius,
                latitude, radius
            )
        )
        rows = cursor.fetchall()
        stations_data = {}
        stations_roads = []
        for row in rows:
            stations_data[row[0]] = Station(
                row[0],
                row[1],
                row[2]
            )
            stations_roads.append(Road(
                row[0],
                row[3],
                row[4],
                row[5]
            ))

        self.__disconnect(cursor)
        return stations_data.values(), stations_roads

    def selectStationsById(
            self,
            st_id
    ):
        cursor = self.__connect()
        cursor.execute(
            DatabaseScripts.selectStationByIdQuery,
            (
                st_id,
            )
        )
        row = cursor.fetchone()
        station = Station(
            row[0],
            row[1],
            row[2]
        )
        self.__disconnect(cursor)
        return station

    def getDestinationsByTrainId(self, train_id):
        destinations = list()
        cursor = self.__connect()

        cursor.execute(
            DatabaseScripts.selectDestinationsByTrain,
            (
                train_id, train_id
            )
        )
        rows = cursor.fetchall()
        for row in rows:
            destinations.append(
                DestinationTrain(
                    oper_date=row[0],
                    st_id=row[1]
                )
            )

        self.__disconnect(cursor)
        return destinations

    def insertDestination(self, destination: Destination):
        curs = self.__connect()
        self.__insertOneDestination(curs, destination)
        self.__disconnect(curs)

    def getActualDestinations(self):
        destinations = list()
        cursor = self.__connect()

        cursor.execute(DatabaseScripts.selectDestinationsActual)
        rows = cursor.fetchall()
        for row in rows:
            destinations.append(
                ActualDestination(
                    train_id=row[1],
                    st_id=row[2],
                    latitude=row[3],
                    longitude=row[4]
                )
            )

        try:
            self.__disconnect(cursor)
        except:
            pass

        return destinations

    def getActualWagons(self, train_id):
        destinations = list()
        cursor = self.__connect()

        cursor.execute(DatabaseScripts.selectActualWagons,
                       (train_id, train_id)
                       )
        rows = cursor.fetchall()
        for row in rows:
            destinations.append(
                ActualWagon(
                    wag_id=row[0],
                    st_id=row[1],
                    latitude=row[2],
                    longitude=row[3]
                )
            )

        try:
            self.__disconnect(cursor)
        except:
            pass
        return destinations

    def __disconnect(self, cursor):
        self.__conn.commit()
        cursor.close()
        self.__conn.close()
        self.__conn = None
