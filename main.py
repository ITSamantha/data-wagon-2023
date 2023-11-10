from flask import Flask, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return 'Hello World'


@app.route('/api/')
def api():
    return 'api'


@app.route('/api/stations/', methods=['GET', 'POST'])
def api_station():
    if request.method == 'GET':
        longitude = request.args.get('longitude')
        latitude = request.args.get('latitude')
        radius = request.args.get('radius')


    elif request.method == 'POST':
        data = request.json
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        radius = data.get('radius')

    response = {
        "success": True,
        "stations": [
            {"longitude": 53.87,
             "latitude": 66.32,
             "id": 15,
             }
        ],
        "network":
            [
                {
                    "from": 15,
                    "to": 24,
                    "dist": 16.8
                }
            ]
    }


if __name__ == "__main__":
    app.run()
