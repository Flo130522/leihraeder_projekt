import folium
import json

# Load data from JSON files
with open('location_data.json', 'r') as file:
    location_data = json.load(file)

with open('start_counts.json', 'r') as file:
    start_counts = json.load(file)

with open('end_counts.json', 'r') as file:
    end_counts = json.load(file)

# Create a base map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Add markers for the stations
for station_id in set(start_counts) | set(end_counts):
    # Extracting name, latitude, and longitude from location_data
    name = location_data[str(station_id)]['name']
    lat = location_data[str(station_id)]['lat']
    long = location_data[str(station_id)]['long']

    # Create popup HTML text with CSS for font and size
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 14px; width:200px; line-height: 1.5;">
        <strong>ID:</strong> {station_id}<br>
        <strong>Name:</strong> {name}<br>
        <strong>Start Count:</strong> {start_counts.get(str(station_id), 'N/A')}<br>
        <strong>End Count:</strong> {end_counts.get(str(station_id), 'N/A')}
    </div>
    """
    iframe = folium.IFrame(html=popup_html, width=250, height=120)
    popup = folium.Popup(iframe, max_width=265)
    marker_color = 'green' if station_id in start_counts and station_id in end_counts else 'blue' if station_id in start_counts else 'red'
    
    # Add marker
    folium.Marker(
        location=[lat, long],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

# Save the map as an HTML file
m.save('sf_bike_stations_map.html')
