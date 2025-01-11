import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def show_page():
# Define pages as functions
    def main_dashboard():
        st.title("Dashboard")

        st.markdown(
            """
            <div style="background-color:#1c1c1c;padding:10px;border-radius:10px">
            <h3 style="color:white;text-align:center;">Welcome to the Unified Dashboard</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("This section can contain other dashboard features.")

    def interactive_map():
        st.image("banner.png", use_container_width=True)
        st.title("Interactive Air Quality Dashboard")

        st.markdown(
            """
            <div style="background-color: #f0f4fa; padding: 20px; border-radius: 5px; margin-bottom: 25px;">
            <p style="text-align: center; color: #000000; font-size: 20px;">
                🌱 Click anywhere on the map to instantly retrieve Latitude and Longitude values. Give it a try and explore the world in coordinates! 🌱 
            </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        center = [20.5937, 78.9629]  # Default center is India
        m = folium.Map(location=center, zoom_start=5)

        # Add a marker for better visualization
        folium.Marker(
            location=center, popup="Default Center", icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # Display the map and capture interaction data
        map_data = st_folium(m, width=1800, height=500, key="folium_map")

        # Display the clicked latitude and longitude
        st.subheader("Latitude and Longitude")
        if map_data is not None and "last_clicked" in map_data and map_data["last_clicked"] is not None:
            lat = map_data["last_clicked"]["lat"]
            lng = map_data["last_clicked"]["lng"]
            st.write(f"**Latitude:** {lat}")
            st.write(f"**Longitude:** {lng}")

            # Fetch air quality data
            API_KEY = "f7b59330-e7a6-4a31-b218-bdf222c03d9c"  # Replace with your actual API key
            BASE_URL = "http://api.airvisual.com/v2/nearest_city"

            params = {"lat": lat, "lon": lng, "key": API_KEY}
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        city = data["data"]["city"]
                        state = data["data"]["state"]
                        country = data["data"]["country"]
                        aqi = data['data']['current']['pollution']['aqius']
                        main_pollutant = data['data']['current']['pollution']['mainus']
                        temp = data['data']['current']['weather']['tp']
                        humidity = data['data']['current']['weather']['hu']
                        pressure = data['data']['current']['weather']['pr']
                        last_update = data['data']['current']['pollution']['ts']

                        st.subheader(f"Air Quality in {city}, {state}, {country}")
                        st.write(f"Last Updated: {datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ')}")
                        st.write(f"Air Quality Index (AQI): {aqi}")
                        st.write(f"Main Pollutant: {main_pollutant}")
                        st.write(f"Temperature: {temp}°C")
                        st.write(f"Humidity: {humidity}%")
                        st.write(f"Pressure: {pressure} hPa")

                    else:
                        st.error(f"Error: {data.get('message', 'Unable to fetch air quality data.')}")

                else:
                    st.error(f"API Response Error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"API Request Failed: {e}")
        else:
            st.write("Click on the map to get latitude and longitude.")

    # Main App Navigation
    def main():
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Dashboard", "Interactive Map"])

        if page == "Dashboard":
            main_dashboard()
        elif page == "Interactive Map":
            interactive_map()

    if __name__ == "__main__":
        main()