import os
from flask import Flask, render_template, request
from utils import get_earthquakes

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    request_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' \
              '2.5_week.geojson'
    data = get_earthquakes(request_url)
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
