from flask import Flask, render_template, request
import folium

app = Flask(__name__)

# Dummy data for locations
locations = [
    {"name": "Location 1", "lat": 19.015831, "lon": 72.82939, "link": "http://example.com/location1"},
    {"name": "Location 2", "lat": 19.014831, "lon": 72.82839, "link": "http://example.com/location2"},
    {"name": "Location 3", "lat": 19.015631, "lon": 72.82439, "link": "http://example.com/location3"},
    {"name": "Location 4", "lat": 19.015331, "lon": 72.82639, "link": "http://example.com/location4"}
]

# Route to home page
@app.route('/')
def home():
    # Create map centered at the first location
    currentLoc = [locations[0]['lat'], locations[0]['lon'] ]
    my_map = folium.Map(location=[currentLoc[0], currentLoc[1]], zoom_start=15)

    # Add markers for each location
    for loc in locations:
        folium.Marker(location=[loc['lat'], loc['lon']], popup=loc['name'], tooltip=loc['name'],
                      icon=folium.Icon(color='blue')).add_to(my_map)

        # Add a circle around the current spot
        folium.Circle(location=[loc['lat'], loc['lon']], radius=500, color='blue', fill=True, fill_color='blue').add_to(my_map)


    # Add a red marker for the current spot
    folium.Marker(currentLoc, icon=folium.Icon(color='red')).add_to(my_map)

    # Convert the map to HTML
    map_html = my_map._repr_html_()

    return render_template('map.html', map_html=map_html)


# Dummy data for stations
stations = {
    "dadar": {"lat": 19.0193, "lon": 72.8429},
    "bandra": {"lat": 19.0544, "lon": 72.8402},
    "andheri": {"lat": 19.1197, "lon": 72.8461}
}

# Route to viewstation page
@app.route('/viewstation')
def viewstation():
    # Get the station name from the query parameters
    station_name = request.args.get('stationname', None)

    # Check if the station name is valid
    if station_name and station_name in stations:
        # If valid, print the station name
        print("Station Name:", station_name)
        # Render the template with the station data
        return render_template('map.html', data=stations[station_name])
    else:
        # If station name is not provided or invalid, return an error message
        return "Invalid station name or station name not provided."

if __name__ == '__main__':
    app.run(debug=True)
