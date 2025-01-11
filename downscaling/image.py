import streamlit as st
import folium
from streamlit_folium import st_folium  # Use st_folium for map interactivity
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import pandas as pd
import os


def show_page():
    layer_path = os.path.join(os.path.dirname(__file__), 'layer3.png')
    jjas_path = os.path.join(os.path.dirname(__file__), 'jjas.csv')
    final_path = os.path.join(os.path.dirname(__file__), 'final_predictions.npz')
    def actual(latitude, longitude):
        try:
            # Load the CSV file
            df = pd.read_csv(jjas_path)

            # Round clicked latitude and longitude to 4 decimal places to match dataset precision
            rounded_lat = round(latitude, 1)
            rounded_lng = round(longitude, 1)

            # Find matching rows in the dataset
            matching_row = df[
                (df['Ground Latitude'].round(1) == rounded_lat) & 
                (df['Ground Longitude'].round(1) == rounded_lng)
            ]

            # If a matching row is found, return the NO2 value; otherwise, return None
            if not matching_row.empty:
                return matching_row['Ground NO2'].values[0]  # Return the first match
            return "No data available at this location."

        except Exception as e:
            return f"Error: {e}"

    def nparray(latitude, longitude):
        if not (8.5 <= latitude <= 37.2 and 70.8 <= longitude <= 94.7):
            return 0

        try:
            # Load the .npz file
            data = np.load(final_path)

            if 'final_predictions' in data.files:
                final_predictions = data['final_predictions']

                # Replace NaN values with 0
                final_predictions = np.nan_to_num(final_predictions, nan=0)

                # Define gridx and gridy (assuming uniform grid for simplicity)
                gridx = np.linspace(0, final_predictions.shape[1] - 1, final_predictions.shape[1])
                gridy = np.linspace(0, final_predictions.shape[0] - 1, final_predictions.shape[0])

                interpolator = RegularGridInterpolator((gridy, gridx), final_predictions)

                # Perform interpolation to get predicted NO2
                point = np.array([[latitude, longitude]])
                if not (gridy.min() <= latitude <= gridy.max() and gridx.min() <= longitude <= gridx.max()):
                    return "Outside interpolation range."
                return interpolator(point)[0]
            else:
                return "Prediction data not found in the file."

        except Exception as e:
            return f"Error: {e}"

    def create_map():
        # Coordinates for the bounds of the image (latitude and longitude of the image corners)
        bounds = [[8.5, 94.7], [33.2, 70.8]]  # Update with your image's lat/lon bounds

        # Initialize Folium map
        m = folium.Map(location=[(8.5 + 33.2) / 2, (70.8 + 94.7) / 2], zoom_start=5)

        # Overlay the Kriging image
        folium.raster_layers.ImageOverlay(
            image=layer_path,  # Path to your kriging image
            bounds=bounds,
            opacity=0.8,  # Adjust opacity for better visibility
            name='Kriging Overlay'
        ).add_to(m)

        # Add LayerControl to toggle layers
        folium.LayerControl().add_to(m)

        # Add LatLngPopup to display latitude and longitude when clicked
        folium.LatLngPopup().add_to(m)

        return m

    # Streamlit code execution starts here
    st.title('Kriging Map Overlay with Coordinate Popup')

    # Create the map
    m = create_map()

    # Display the map using streamlit-folium
    map_data = st_folium(m, width=750, height=500, key="folium-map")

    if map_data is not None and "last_clicked" in map_data and map_data["last_clicked"] is not None:
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]

        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {lng}")
        st.write(f'Actual Ground NO2: {actual(lat, lng)}')
        st.write(f"Predicted NO2: {nparray(lat, lng)}")

    # Additional instructions
    st.info('Click anywhere on the map to see the latitude and longitude.')
