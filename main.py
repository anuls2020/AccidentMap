import folium
from folium.plugins import MarkerCluster
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Load the file containing the country name and the coordinates
def load_data():
    try:
        return pd.read_csv("accidents.csv", sep=';', encoding='unicode_escape')
    except FileNotFoundError:
        return "File does not exist."

@app.route('/')
def index():
    data = load_data()
    # print(data.head(5))

    # Create the folium map centered around the Europe
    m = folium.Map(location=[34, -86], zoom_start=4)

    # Crete Marker Cluster Object
    marker_cluster = MarkerCluster().add_to(m)

    # # Add country names as markers to the MarkerCluster by loop over the data
    for _, row in data.iterrows():
        folium.Marker(
            location=[row["LATITUDE"], row["LONGITUD"]],
            popup=row["MAN_COLLNAME"],
            tooltip=row["MAN_COLLNAME"],
        ).add_to(marker_cluster)

    # Save the map as HTML file inside the templates folder
    m.save("templates/AccidentMap.html")

    return render_template("AccidentMap.html")


if __name__ == '__main__':
    app.run(debug=True)