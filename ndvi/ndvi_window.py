import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os

# Load the NDVI, Elevation, and Population Density data
# Replace with the actual file paths
def show_page():
    ndvi_path = os.path.join(os.path.dirname(__file__), 'sorted_NDVI_data.csv')
    elevation_path = os.path.join(os.path.dirname(__file__), 'sorted_India_Elevation.csv')
    population_path = os.path.join(os.path.dirname(__file__), 'acc_india_population_data.csv')
    
    ndvi_df = pd.read_csv(ndvi_path)  # NDVI data with Latitude, Longitude, NDVI
    elevation_df = pd.read_csv(elevation_path)  # Elevation data with Longitude, Latitude, Elevation
    population_df = pd.read_csv(population_path)  # Population Density data with Longitude, Latitude, Population Density
    
    st.title("Interactive India Map with NDVI, Elevation, and Population Density")
    st.write("Click on the map to display latitude, longitude, NDVI, Elevation, and Population Density.")

    # Add custom CSS for the map to change cursor to pointer when hovering and dragging
    st.markdown("""
        <style>
        .leaflet-container {
            cursor: pointer !important;
        }
        .leaflet-container.leaflet-grab {
            cursor: pointer !important;
        }
        .leaflet-container.leaflet-grabbing {
            cursor: pointer !important;
        }
        </style>
    """, unsafe_allow_html=True)

        # Create a map centered on India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

        # Display the map and capture click events
    output = st_folium(m, width=700, height=500)

        # Check if output is not None and contains 'last_clicked'
    if output:
            last_clicked = output.get("last_clicked")
            if last_clicked:
                lat = last_clicked["lat"]
                lon = last_clicked["lng"]
                st.success(f"Clicked")
                
                # Get NDVI, Elevation, and Population Density for the clicked location
                ndvi_value = get_nearest_value(ndvi_df, lat, lon, 'NDVI')
                elevation_value = get_nearest_value(elevation_df, lat, lon, 'Elevation')
                population_density_value = get_nearest_value(population_df, lat, lon, 'Population Density')
                
                # Display the values
                st.write(f"Latitude : {lat}")
                st.write(f"Longitude : {lon}")
                st.write(f"NDVI : {ndvi_value}")
                st.write(f"Elevation : {elevation_value} meters")
                st.write(f"Population Density : {population_density_value}")
                
            else:
                st.info("Click on the map to display latitude and longitude.")
    else:
            st.info("No map interaction detected yet.")

def get_nearest_value(df, lat, lon, column):
        # Find the row with the closest latitude and longitude
        df['distance'] = (df['Latitude'] - lat)**2 + (df['Longitude'] - lon)**2
        closest_row = df.loc[df['distance'].idxmin()]
        return closest_row[column]
