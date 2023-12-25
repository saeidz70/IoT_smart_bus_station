from flask import Flask, render_template, request
from dataProvider import *
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/station')
def get_station():
    station = request.args.get('station')
    print("station is ", station)

    if not bool(station.strip()):
        station = "station_1"

    station_data = DataProvider().get_data(station)

    if not station_data['response'] == 200:
        return render_template('not_found.html')

    return render_template('station.html',
                           station_name=station_data["station"],
                           temperature=station_data["temperature"],
                           humidity=station_data["humidity"],
                           cooler=station_data["cooler"],
                           heater=station_data["heater"],
                           dehumidifier=station_data["dehumidifier"],
                           light=station_data["light"])


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
