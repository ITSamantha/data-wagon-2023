import datetime
import os

import flask
from flask import Flask, request

from bootstrap import bootstrap
from database.Repository import Repository
from models.Destination import Destination
from simulator import file_processing
from flask_cors import CORS

from utils.titles import generate_meme_name, generate_random_time

app = Flask(__name__)
cors = CORS(app)
app.debug = True
bootstrap()

r = Repository(
    os.getenv('DATABASE_URL'),
    os.getenv('DATABASE_PASSWORD'),
)

@app.route('/')
def index():
    return 'Hello World'


@app.route('/api/')
def api():
    return 'api'


@app.route('/api/stations/', methods=['GET'])
def api_station():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    radius = request.args.get('radius')
    return r.getStationsJson(float(longitude), float(latitude), float(radius))

@app.route('/api/train_destinations/', methods=['GET'])
def get_train_destinations():
    response = [
        {'station': generate_meme_name(1), 'time': generate_random_time()},
        {'station': generate_meme_name(2), 'time': generate_random_time()},
        {'station': generate_meme_name(3), 'time': generate_random_time()},
        {'station': generate_meme_name(4), 'time': generate_random_time()},
        {'station': generate_meme_name(5), 'time': generate_random_time()},
        {'station': generate_meme_name(6), 'time': generate_random_time()},
        {'station': generate_meme_name(7), 'time': generate_random_time()},
        {'station': generate_meme_name(8), 'time': generate_random_time()},
        {'station': generate_meme_name(9), 'time': generate_random_time()},
        {'station': generate_meme_name(10), 'time': generate_random_time()},
        {'station': generate_meme_name(11), 'time': generate_random_time()},
    ]
    response = flask.jsonify(response)
    return response
    # train_id = request.args.get('train_id')
    # return r.getDestinationsByTrainId(train_id)


@app.route('/api/actual_destinations/', methods=['GET'])
def get_actual_destinations():
    return r.getActualDestinations()

@app.route('/api/actual_wagons/', methods=['GET'])
def get_actual_wagons():
    train_id = request.args.get('train_id')
    return r.getActualWagons(train_id)


@app.route('/api/add_dest', methods=['POST'])
def add_destination():
    response = {}
    data = request.get_json()
    print(data)
    destination = data['destination']

    wag_id = destination['WAGNUM']
    oper_date = destination['OPERDATE']

    disl_id = destination['ST_ID_DISL']
    dest_id = destination['ST_ID_DEST']
    train_index = str(destination['TRAIN_INDEX']).split('-')
    train_id = train_index[1]
    form_st_id = train_index[0]
    target_st_id = train_index[2]

    date = datetime.datetime.strptime(oper_date, file_processing.DATE_FORMAT)
    print('aa')
    r.addDestination(
        Destination(
            wag_id=int(wag_id),
            oper_date=date,
            disl_st_id=int(disl_id),
            dest_st_id=int(dest_id),
            train_id=int(train_id),
            form_st_id=int(form_st_id),
            target_st_id=int(target_st_id),
            id=0
        )
    )

    response['success'] = True
    return response


if __name__ == "__main__":
    app.run()
