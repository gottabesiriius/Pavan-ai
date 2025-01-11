import streamlit as st
from streamlit_folium import st_folium
import folium
import math
import pandas as pd
from folium.plugins import HeatMap
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf


def show_page():
    print(tf.__version__)
    
    # Load the neural network model
    model = load_model("0.875-synthetic-1lakh-model.h5")

    # Step 1: Read the CSV file into a pandas DataFrame
    df = pd.read_csv('only_hyderabad.csv')
    x = {}
    df['modified'] = df['NO2'] * 1e6
    df.to_csv('only_hyderabad.csv', index=False)

    # Set the page configuration
    
    st.image("banner.png", use_container_width=True)

    # Title of the app
    st.title("Predict NO2 at Clicked Location")
    
    st.markdown(
        """
        <div style="
            background-color: #f0f4fa; 
            padding: 20px; 
            border-radius: 5px; 
            margin-bottom: 25px;">
            <p style="text-align: center; color: #000000; font-size: 20px;">
                ✨ This page provides an interactive way to predict NO2 values. Click on any region, and let the magic unfold 📊
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Define the stations
    stations = [
        {"name": "Central University", "lat": 17.4559, "long": 78.3324, "no2": 20.02},
        {"name": "ECIL Kapra", "lat": 17.4799, "long": 78.5785, "no2": 21.8},
        {"name": "ICRISAT Patancheru", "lat": 17.5126, "long": 78.2541, "no2": 26.21},
        {"name": "IDA Pashamylaram", "lat": 17.5443, "long": 78.3693, "no2": 32.2},
        {"name": "IITH Kandi", "lat": 17.5449, "long": 78.3444, "no2": 8.54},
        {"name": "Kokapet", "lat": 17.3894, "long": 78.3772, "no2": 6.39},
        {"name": "Kompally Municipal Office", "lat": 17.5542, "long": 78.4848, "no2": 12.15},
        {"name": "Nacharam_TSIIC IALA", "lat": 17.4293, "long": 78.5484, "no2": 9.03},
        {"name": "New Malakpet", "lat": 17.3826, "long": 78.5016, "no2": 10.89},
        {"name": "Ramachandrapuram", "lat": 17.4919, "long": 78.3106, "no2": 10.12},
        {"name": "Sanathnagar", "lat": 17.4517, "long": 78.4353, "no2": 21.26},
        {"name": "Somajiguda", "lat": 17.4256, "long": 78.4483, "no2": 37.71},
        {"name": "Zoo Park", "lat": 17.3599, "long": 78.4679, "no2": 59.77},
    ]


    # Haversine formula to calculate the distance between two lat-long points
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    # Initialize session state
    if "clicked_lat_lng" not in st.session_state:
        st.session_state["clicked_lat_lng"] = None
    if "process_button_clicked" not in st.session_state:
        st.session_state["process_button_clicked"] = False

    col1, col2 = st.columns(2)

    with col1:
        # Create the first map
        m1 = folium.Map(location=[17.4188, 78.4753], zoom_start=11)

        # Add station markers
        for station in stations:
            folium.Marker(
                location=[station["lat"], station["long"]],
                popup=f"{station['name']} - NO2: {station['no2']} ug/m³",
                icon=folium.Icon(color="blue")
            ).add_to(m1)

        # Add rectangles from the dataset
        for _, row in df.iterrows():
            folium.Rectangle(
                bounds=[
                    [row['latitude'] - 0.0255, row['longitude'] - 0.0157],
                    [row['latitude'] + 0.0255, row['longitude'] + 0.0157]
                ],
                color="red",
                fill_color="red",
                fill_opacity=0.3,
                tooltip=f'NO2: {round(row["modified"], 2)} ug/m³'
            ).add_to(m1)

        # Add heatmap
        heat_data = [[row['latitude'], row['longitude'], row['modified']] for _, row in df.iterrows()]
        HeatMap(heat_data).add_to(m1)

        # Display the map
        map_data = st_folium(m1, width=700, height=500, key="folium_map")

        if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
            st.session_state["clicked_lat_lng"] = map_data["last_clicked"]

        if st.button("Find Nearest Station and Predict NO2"):
            st.session_state["process_button_clicked"] = True

    if st.session_state.get("clicked_lat_lng"):
        lat = st.session_state["clicked_lat_lng"]["lat"]
        lng = st.session_state["clicked_lat_lng"]["lng"]

        if st.session_state["process_button_clicked"]:
            # Find the nearest station
            nearest_station = None
            min_distance = float("inf")

            for station in stations:
                distance = haversine(lat, lng, station["lat"], station["long"])
                if distance < min_distance:
                    nearest_station = station
                    min_distance = distance

        # Predict NO2 at the clicked location using the model
            model_input = np.array([[lat, lng, nearest_station['lat'], nearest_station['long'], nearest_station['no2'], min_distance]])
            predicted_no2 = float(model.predict(model_input)[0][0])  # Convert to native Python float

            with col2:
                # Create the second map
                m2 = folium.Map(location=[17.4188, 78.4753], zoom_start=11)
                for _, row in df.iterrows():
                    latitude, longitude = row['latitude'], row['longitude']
                    folium.Rectangle(
                        bounds=[
                            [row['latitude'] - 0.0255, row['longitude'] - 0.0157],
                            [row['latitude'] + 0.0255, row['longitude'] + 0.0157]
                        ],
                        color="red",
                        fill_color="red",
                        fill_opacity=0.3,
                        tooltip=f'[{row["latitude"]},{longitude}] : {round(row["modified"], 2)} ug/m³'
                    ).add_to(m2)
                
                heat_data = [[row['latitude'], row['longitude'], row['modified']] for _, row in df.iterrows()]
                HeatMap(heat_data).add_to(m2)
                # Add the nearest station marker
                folium.Marker(
                    location=[nearest_station["lat"], nearest_station["long"]],
                    popup=f"Nearest Station: {nearest_station['name']}\n"
                        f"Lat: {nearest_station['lat']}, Long: {nearest_station['long']}\n"
                        f"Distance: {min_distance:.2f} km\nNO2: {nearest_station['no2']} ug/m³",
                    icon=folium.Icon(color="green"),
                ).add_to(m2)

                # Add a heatmap for the predicted NO2 value
    # Add the heatmap for predicted NO2 with increased radius
                HeatMap([[lat, lng, predicted_no2]], radius=50).add_to(m2)

                # Add a marker for the clicked location
                folium.Marker(
                    location=[lat, lng],
                    popup=f"Predicted NO2: {predicted_no2:.2f} ug/m³",
                    icon=folium.Icon(color="red"),
                ).add_to(m2)

                # Display the second map
                st_folium(m2, width=700, height=500, key="predicted_map")
            st.success(f"**predicted no2 at --> ( lat - {lat} , long --> {lng} ) is :   {predicted_no2}ug/m³**")
