"""
Plot earthquake data from US Geological survey.
"""
import datetime
import io
import os

import plotly.graph_objs as go
from flask import Flask, Response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from plotly import offline

from utils import get_earthquakes

app = Flask(__name__)


# TODO (D. Rodriguez 2021-04-06): Refactor code
def create_figure(recent_eq_data):
    """Create plot."""
    # fig = Figure()
    # axis = fig.add_subplot(1, 1, 1)
    # xs = range(100)
    # ys = [random.randint(1, 50) for x in xs]
    # axis.plot(xs, ys)

    # TODO (D. Rodriguez 2021-04-06): Hide this in Env Variable
    mapbox_access_token = 'pk.eyJ1Ijoid2FzaGlyaWNhbiIsImEiOiJja2gyeG9kdWUxYXJoMnJybmlweXg2aTRiIn0.AnaSkQ6ZFXEHsd4kWYoQxw'  # open(".mapbox_token").read()

    # Get chart title from json data
    title = recent_eq_data['metadata']['title']
    data_date = datetime.datetime.fromtimestamp(recent_eq_data['metadata']['generated'] / 1e3)

    header = f"{title} (Data from {data_date.strftime('%m/%d/%Y, %H:%M:%S')})"

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
            eq_date = datetime.datetime.fromtimestamp(eq_dict['properties']['time'] / 1e3)

        #     hover_texts.append(
        #             f"<a href={eq_details_url} style='color: black'>{eq_dict['properties']['title']}-{eq_date}</a>")
            hover_texts.append(f"{eq_dict['properties']['title']}<br />"
                               f"{eq_date.strftime('%m/%d/%Y, %H:%M:%S')}<br />")


    fig = go.Figure(go.Scattermapbox(
            lon=longitudes,
            lat=latitudes,
            text=hover_texts,
            marker=go.scattermapbox.Marker(
                    {
                        'size': [5 * magnitude for magnitude in magnitudes],
                        'color': magnitudes,
                        'colorscale': 'sunset',
                        'reversescale': True,
                        'colorbar': {'title': 'Magnitude'},
                        }
                    ),
            ))

    fig.update_layout(
            title_text=header,
            hovermode='closest',
            mapbox_style='carto-positron',
            mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=go.layout.mapbox.Center(
                            lat=18.23,
                            lon=-66.48,
                            ),
                    pitch=0,
                    zoom=8.5,
                    )
            )
    # TODO (D. Rodriguez 2021-04-09): Create image in html page and have
    #  flask route render it.
    filename = 'recent_earthquakes.html'
    offline.plot(fig, filename=f'templates/{filename}')

    return filename


# TODO (D. Rodriguez 2021-04-06): Add Home route with details about page
# TODO (D. Rodriguez 2021-04-06): Add user input for search parameters
#  (timeframe and magnitude)
@app.route('/', methods=['GET', 'POST'])
def index():
    """App index page."""
    request_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' \
              '2.5_week.geojson'

    recent_eq_data = get_earthquakes(request_url)

    filename = create_figure(recent_eq_data)
    # offline.plot(fig, filename='templates/puerto_rico_earthquakes.html')

    #
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')

    return render_template(filename)


# TODO (D. Rodriguez 2021-04-06): Add map template and route.
# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# FIXME (2024-02-23): When running it open 2 browser windows?
# LEARN (2024-02-23): Figure out why this is happening
if __name__ == '__main__':
    app.run(debug=False)
