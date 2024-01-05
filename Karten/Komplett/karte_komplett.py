import folium
import pandas as pd
import json

# Funktion zum Erstellen eines stilisierten Popups
def styled_popup(station_id, name, city, dock_count, start_count, end_count):
    return f"""
    <div style="font-family: 'Arial', sans-serif; font-size: 12px; 
                border: 1px solid black; border-radius: 5px; overflow: hidden; 
                box-shadow: 3px 3px 3px rgba(0,0,0,0.2);">
        <div style="background-color: blue; padding: 5px; text-align: center; 
                    font-weight: bold; color: white;">
            {name} (ID: {station_id})
        </div>
        <div style="padding: 5px;">
            <p><strong>City:</strong> {city}</p>
            <p><strong>Dock count:</strong> {dock_count}</p>
            <p><strong>Start count:</strong> {start_count}</p>
            <p><strong>End count:</strong> {end_count}</p>
        </div>
    </div>
    """

import folium
import pandas as pd
import json

# Funktion zum Erstellen eines stilisierten Popups mit Farbanpassung
def styled_popup(station_id, name, city, dock_count, start_count, end_count, marker_color):
    return f"""
    <div style="font-family: 'Arial', sans-serif; font-size: 12px; 
                border: 1px solid black; border-radius: 5px; overflow: hidden; 
                box-shadow: 3px 3px 3px rgba(0,0,0,0.2);">
        <div style="background-color: {marker_color}; padding: 5px; text-align: center; 
                    font-weight: bold; color: white;">
            {name} (ID: {station_id})
        </div>
        <div style="padding: 5px;">
            <p><strong>City:</strong> {city}</p>
            <p><strong>Dock count:</strong> {dock_count}</p>
            <p><strong>Start count:</strong> {start_count}</p>
            <p><strong>End count:</strong> {end_count}</p>
        </div>
    </div>
    """

# Farbkodierung für die Städte
city_colors = {
    "San Jose": "red",
    "Redwood City": "blue",
    "Mountain View": "green",
    "Palo Alto": "purple",
    "San Francisco": "orange"
    # Fügen Sie hier weitere Städte und Farben hinzu, falls nötig
}

# Pfad zu Ihren JSON-Dateien
path_to_stations = r"C:\Users\Admin\OneDrive\Desktop\station_202401041651.json"
path_to_start_usage = r"C:\Users\Admin\OneDrive\Desktop\_Nutzung_Auslastung_der_Stationen_Start_SELECT_start_station_nam_202401041652.json"
path_to_end_usage = r"C:\Users\Admin\OneDrive\Desktop\_Ziel_SELECT_end_station_name_COUNT_as_usage_count_FROM_trip_GRO_202401041652.json"

# Laden der Daten
with open(path_to_stations) as file:
    stations_data = json.load(file)
    stations_df = pd.DataFrame(stations_data['station'])

with open(path_to_start_usage) as file:
    start_data = json.load(file)
    start_usage_df = pd.DataFrame(start_data[next(iter(start_data))])

with open(path_to_end_usage) as file:
    end_data = json.load(file)
    end_usage_df = pd.DataFrame(end_data[next(iter(end_data))])

# Umwandlung in Wörterbücher für schnelleren Zugriff
start_usage_dict = start_usage_df.set_index('start_station_name')['usage_count'].to_dict()
end_usage_dict = end_usage_df.set_index('end_station_name')['usage_count'].to_dict()

# Erstellung der Karte
m = folium.Map(location=[37.32973, -121.90178], zoom_start=12)

# Hinzufügen der Marker mit den stilisierten Popups
for index, row in stations_df.iterrows():
    station_id = row['id']
    name = row['name']
    city = row['city']
    dock_count = row['dock_count']
    start_count = start_usage_dict.get(name, 'N/A')
    end_count = end_usage_dict.get(name, 'N/A')
    marker_color = city_colors.get(city, "gray")  # Farbe aus dem city_colors Wörterbuch

    # Erstellen des Popup-HTML-Textes mit der Hilfsfunktion
    popup_html = styled_popup(station_id, name, city, dock_count, start_count, end_count, marker_color)
    iframe = folium.IFrame(popup_html, width=300, height=150)  # Größe des Popups
    popup = folium.Popup(iframe, max_width=300)
    
    marker = folium.Marker(
        [row['lat'], row['long']],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    )
    m.add_child(marker)

# Speichern der Karte
m.save('station_map.html')


# Laden der Daten
with open(path_to_stations) as file:
    stations_data = json.load(file)
    stations_df = pd.DataFrame(stations_data['station'])

with open(path_to_start_usage) as file:
    start_data = json.load(file)
    start_usage_df = pd.DataFrame(start_data[next(iter(start_data))])

with open(path_to_end_usage) as file:
    end_data = json.load(file)
    end_usage_df = pd.DataFrame(end_data[next(iter(end_data))])

# Umwandlung in Wörterbücher
start_usage_dict = start_usage_df.set_index('start_station_name')['usage_count'].to_dict()
end_usage_dict = end_usage_df.set_index('end_station_name')['usage_count'].to_dict()

# Erstellung der Karte
m = folium.Map(location=[37.32973, -121.90178], zoom_start=12)
marker_colors = {
    "San Jose": "red", 
    "Redwood City": "blue", 
    "Mountain View": "green", 
    "Palo Alto": "purple", 
    "San Francisco": "orange"
}

# Erstellung der Marker-Gruppen
groups = {city: folium.FeatureGroup(name=city) for city in marker_colors.keys()}

# Hinzufügen der Marker mit den stilisierten Popups
for index, row in stations_df.iterrows():
    station_id = row['id']
    name = row['name']
    city = row['city']
    dock_count = row['dock_count']
    start_count = start_usage_dict.get(name, 'N/A')
    end_count = end_usage_dict.get(name, 'N/A')
    color = city_colors.get(city, "gray")  # Passen Sie die Farbe basierend auf der Stadt an

    # Erstellen des Popup-HTML-Textes mit der Hilfsfunktion
    popup_html = styled_popup(station_id, name, city, dock_count, start_count, end_count, color)
    iframe = folium.IFrame(popup_html, width=300, height=200)  # Größe des Popups
    popup = folium.Popup(iframe, max_width=300)
    
    marker = folium.Marker(
        [row['lat'], row['long']],
        popup=popup,
        icon=folium.Icon(color=color)
    )
    m.add_child(marker)

# Hinzufügen der Gruppen zur Karte
for group in groups.values():
    m.add_child(group)

# LayerControl hinzufügen, um die Sichtbarkeit der Marker-Gruppen zu steuern
folium.LayerControl().add_to(m)

# Speichern der Karte
m.save('station_map.html')
