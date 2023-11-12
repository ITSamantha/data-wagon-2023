import json
import math
import os
import time

import requests
import geojson

from bootstrap import bootstrap
from database.Repository import Repository
from utils.titles import generate_meme_name

all_coords = []


progress = 0

def send_osrm_request(start_coords, end_coords):
    global progress
    progress += 1
    base_url = "http://router.project-osrm.org/route/v1/rail/"
    start_coords_str = ",".join(map(str, start_coords[::-1]))  # Reverse order for OSRM format
    end_coords_str = ",".join(map(str, end_coords[::-1]))
    url = f"{base_url}{start_coords_str};{end_coords_str}?geometries=geojson"
    response = requests.get(url)

    if progress % 41 == 0:
        print(str(progress / 41) + '%')

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        print(f"Error: {response.json()}")
        return None
    else:
        print("PANIC")
        print(response.status_code)

def get_partial_geo_information(road):
    response = send_osrm_request((road[1], road[0]), (road[3], road[2]))
    if response and response['code'] == 'Ok':
        coords = response['routes'][0]['geometry']['coordinates']
        all_coords.append({
            'coords': [[road[0], road[1]]] + coords + [[road[2], road[3]]],
            'started_at': road[4],
            'finished_at': road[5],
        })
    else:
        all_coords.append({
            'coords': [[road[0], road[1]]] + [[road[2], road[3]]],
            'started_at': road[4],
            'finished_at': road[5],
        })



def read_geo_data_from_api():
    bootstrap()
    r = Repository(
        os.getenv('DATABASE_URL'),
        os.getenv('DATABASE_PASSWORD'),
    )
    roads = r.getAllRoads()

    for index, road in enumerate(roads):
        get_partial_geo_information(road)
        time.sleep(0.01)


def routes_to_geo():
    bootstrap()
    with open(os.getenv('COORDS_RAW_PATH'), 'r') as file:
        all_coords = json.load(file)
        features = []
        for road in all_coords:
            coordinates = road['coords']
            if math.isnan(coordinates[0][0]) or math.isnan(coordinates[1][0]):
                continue
            properties = {
                'started_at': road['started_at'],
                'finished_at': road['finished_at'],
            }
            feature = geojson.Feature(geometry=geojson.LineString(coordinates), properties=properties)
            features.append(feature)
        feature_collection = geojson.FeatureCollection(features)
        with open(os.getenv('COORDS_PATH'), 'w') as file:
            geojson.dump(feature_collection, file)


def points_to_geo():
    bootstrap()
    r = Repository(
        os.getenv('DATABASE_URL'),
        os.getenv('DATABASE_PASSWORD'),
    )
    stations = json.loads(r.getStationsJson(0, 0, 10000))
    point_features = []
    for station in stations['stations']:
        point_properties = {
            'title': generate_meme_name(station['id']),
            'st_id': station['id']
        }
        point_feature = geojson.Feature(geometry=geojson.Point((station['longitude'], station['latitude'])), properties=point_properties)
        point_features.append(point_feature)
    point_feature_collection = geojson.FeatureCollection(point_features)
    with open(os.getenv('COORDS_POINT_PATH'), 'w') as point_file:
        geojson.dump(point_feature_collection, point_file)


points_to_geo()
