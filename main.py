# --------------------------------------------------------------------------- #
# D. Rodriguez, 2020-10-27, File Created.
# Plot recent earthquake activity in Puerto Rico
# --------------------------------------------------------------------------- #

import requests
import plotly.graph_objs as go
from plotly import offline

# Extra credit: Get recent earthquake data from USGS.
request_url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' \
              '2.5_week.geojson'

response = requests.get(request_url)
recent_eq_data = response.json()

# Get chart title from json data
title = recent_eq_data['metadata']['title']

# Extract earthquake dictionaries from json data
all_eq_dicts = recent_eq_data['features']
# print(len(all_eq_dicts))

# Get earthquake magnitudes and store them in a list.
magnitudes, longitudes, latitudes, hover_texts = [], [], [], []
for eq_dict in all_eq_dicts:

    # Filter for Puerto Rico in earthquake title
    if 'Puerto Rico' in eq_dict['properties']['title']:
        # Refactor to use values directly and not saving to temporary variables
        magnitudes.append(eq_dict['properties']['mag'])
        longitudes.append(eq_dict['geometry']['coordinates'][0])
        latitudes.append(eq_dict['geometry']['coordinates'][1])
        hover_texts.append(eq_dict['properties']['title'])

# This should not be public!
mapbox_access_token = 'pk.eyJ1Ijoid2FzaGlyaWNhbiIsImEiOiJja2gyeG9kdWUxYXJoMnJybmlweXg2aTRiIn0.AnaSkQ6ZFXEHsd4kWYoQxw'  # open(".mapbox_token").read()

# Define chart in a way that is better to customize it.
fig = go.Figure(go.Scattermapbox(
        lon=longitudes,
        lat=latitudes,
        text=hover_texts,
        marker=go.scattermapbox.Marker(
                {
                    'size': [5 * magnitude for magnitude in magnitudes],
                    'color': magnitudes,
                    'colorscale': 'Viridis',
                    'reversescale': True,
                    'colorbar': {'title': 'Magnitude'},
                    }
                ),
        ))

fig.update_layout(
        title_text=title,
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

offline.plot(fig, filename='puerto_rico_earthquakes.html')
