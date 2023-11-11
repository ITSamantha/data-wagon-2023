import datetime
import os

from flask import Flask, request

from backend.models.Destination import Destination
from backend.utils.Bootstrap import bootstrap
from database.Repository import Repository

app = Flask(__name__)
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
    return r.getStationsJson(longitude, latitude, radius)

@app.route('/api/train_destinations/', methods=['GET'])
def get_train_destinations():
    train_id = request.args.get('train_id')
    return r.getDestinationsByTrainId(train_id)

@app.route('/api/add_dest', methods=['POST'])
def add_destination():
    input_json = dict(request.form)
    print(input_json)
    wag_id =  input_json['wagnum']

    oper_date =  input_json['operdate']
    disl_id =  input_json['st_id_disl']
    dest_id =  input_json['st_id_dest']
    train_index = str( input_json['train_index']).split('-')
    train_id = train_index[1]
    form_st_id = train_index[0]
    target_st_id = train_index[2]

    date = datetime.datetime.strptime(oper_date, '%Y-%m-%d %H:%M:%S')
    try:
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
    except:
        pass

    response = {'success': True}
    return response


if __name__ == "__main__":
   app.run()

