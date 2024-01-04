import folium

# Koordinaten der Stationen
station_coords = {
    70: [37.776617, -122.395260],
    50: [37.795392, -122.394203],
    77: [37.789625, -122.400811],
    55: [37.789756, -122.394643],
    60: [37.804770, -122.403234],
    61: [37.780526, -122.390288]
}

# Namen der Stationen
station_names = {
    70: "San Francisco Caltrain (Townsend at 4th)",
    50: "Harry Bridges Plaza (Ferry Building)",
    77: "Market at Sansome",
    55: "Temporary Transbay Terminal (Howard at Beale)",
    60: "Embarcadero at Sansome",
    61: "2nd at Townsend"
}

# Anzahlen der Starts und Ziele
start_counts = {70: 28338, 50: 16849, 77: 14953, 55: 14207, 60: 13504}
end_counts = {70: 32336, 77: 16837, 50: 15822, 60: 15072, 61: 12981}

# Erstellen einer Grundkarte
m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Hinzufügen der Marker für die Stationen
for station_id in set(start_counts) | set(end_counts):
    # Erstellen des Popup-HTML-Textes mit CSS für Schriftart und -größe
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 14px; width:200px; line-height: 1.5;">
        <strong>ID:</strong> {station_id}<br>
        <strong>Name:</strong> {station_names.get(station_id, 'N/A')}<br>
        <strong>Anzahl Start:</strong> {start_counts.get(station_id, 'N/A')}<br>
        <strong>Anzahl Ziel:</strong> {end_counts.get(station_id, 'N/A')}
    </div>
    """
    iframe = folium.IFrame(html=popup_html, width=250, height=120)
    popup = folium.Popup(iframe, max_width=265)
    marker_color = 'green' if station_id in start_counts and station_id in end_counts else 'blue' if station_id in start_counts else 'red'
    folium.Marker(
        location=station_coords[station_id],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

# Speichern der Karte als HTML-Datei
m.save('sf_bike_stations_map.html')
