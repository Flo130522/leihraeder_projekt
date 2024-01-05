import folium

# Koordinaten und Namen der Top 5 Start- und Zielstationen
location_data = {
    "70": {"name": "San Francisco Caltrain (Townsend at 4th)", "lat": 37.776615, "long": -122.39526},
    "69": {"name": "San Francisco Caltrain 2 (330 Townsend)", "lat": 37.7766, "long": -122.39547},
    "50": {"name": "Harry Bridges Plaza (Ferry Building)", "lat": 37.79539, "long": -122.3942},
    "60": {"name": "Embarcadero at Sansome", "lat": 37.80477, "long": -122.40324},
    "55": {"name": "Temporary Transbay Terminal (Howard at Beale)", "lat": 37.789757, "long": -122.394646},
    "61": {"name": "2nd at Townsend", "lat": 37.780525, "long": -122.39029}
}

# Anzahlen der Starts und Ziele
start_counts = {
    "70": 49092,
    "69": 33742,
    "50": 32934,
    "60": 27713,
    "55": 26089
}
end_counts = {
    "70": 63179,
    "69": 35117,
    "50": 33193,
    "60": 30796,
    "61": 28529
}

# Erstellen einer Grundkarte
m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Hinzufügen der Marker für die Stationen
for station_id in set(start_counts) | set(end_counts):
    # Extrahieren von Name, Breitengrad und Längengrad aus location_data
    name = location_data[station_id]['name']
    lat = location_data[station_id]['lat']
    long = location_data[station_id]['long']

    # Erstellen des Popup-HTML-Textes mit CSS für Schriftart und -größe
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 14px; width:200px; line-height: 1.5;">
        <strong>ID:</strong> {station_id}<br>
        <strong>Name:</strong> {name}<br>
        <strong>Start Count:</strong> {start_counts.get(station_id, 'N/A')}<br>
        <strong>End Count:</strong> {end_counts.get(station_id, 'N/A')}
    </div>
    """
    iframe = folium.IFrame(html=popup_html, width=250, height=120)
    popup = folium.Popup(iframe, max_width=265)
    marker_color = 'green' if station_id in start_counts and station_id in end_counts else 'blue' if station_id in start_counts else 'red'
    
    # Marker hinzufügen
    folium.Marker(
        location=[lat, long],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

# Speichern der Karte als HTML-Datei
m.save('sf_bike_stations_map.html')
