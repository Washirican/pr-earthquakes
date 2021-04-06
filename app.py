import os
from flask import Flask, render_template, request
from utils import get_earthquakes

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    request_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' \
              '2.5_week.geojson'
    recent_eq_data = get_earthquakes(request_url)

    # Get chart title from json data
    title = recent_eq_data['metadata']['title']

    # Extract earthquake dictionaries from json data
    all_eq_dicts = recent_eq_data['features']

    # Get earthquake magnitudes and store them in a list.
    magnitudes, longitudes, latitudes, hover_texts = [], [], [], []
    for eq_dict in all_eq_dicts:

        # Filter for Puerto Rico in earthquake title
        if 'Puerto Rico' in eq_dict['properties']['title']:
            eq_id = eq_dict['id']
            eq_details_url = f'https://earthquake.usgs.gov/earthquakes/eventpage/{eq_id}/executive'

            magnitudes.append(eq_dict['properties']['mag'])
            longitudes.append(eq_dict['geometry']['coordinates'][0])
            latitudes.append(eq_dict['geometry']['coordinates'][1])
            # hover_texts.append(eq_dict['properties']['title'])

            # TODO (D. Rodriguez 2021-01-31): Make link work.
            #  Reference https://www.youtube.com/watch?v=7R7VMSLwooo&feature=youtu.be&ab_channel=CharmingData
            hover_texts.append(
                f"<a href={eq_details_url}>{eq_dict['properties']['title']}</a>")


    return render_template('index.html', data=all_eq_dicts)


if __name__ == '__main__':
    app.run()
