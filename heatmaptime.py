import streamlit as st
import folium
from folium.plugins import HeatMapWithTime
import pandas as pd

# Load your data
def heatmap_timebased(selected_city,data_type):
    st.subheader(f"NO2 Heatmap for {data_type} of {selected_city} :")
    satellite_data = pd.read_csv('modified_satellite_data2.csv')
    ground_data = pd.read_csv('ground_data2.csv')

    # Convert date columns to datetime
    satellite_data['Date'] = pd.to_datetime(satellite_data['Date'], format='%d-%m-%Y %H:%M')
    ground_data['Date'] = pd.to_datetime(ground_data['Date'], format='%d-%m-%Y %H:%M')

    # Streamlit App
    cities = sorted(set(satellite_data['City']).union(set(ground_data['City'])))

    # Initialize heatmap data and time index
    heatmap_data = []

    # Process based on selected data type
    if data_type == "Satellite Data":
        filtered_data = satellite_data[satellite_data['City'] == selected_city]
        heatmap_column = 'NO2'  # Assuming NO2 is available in satellite data
    else:
        filtered_data = ground_data[ground_data['City'] == selected_city]
        heatmap_column = 'NO2'  # Ground data also contains NO2

    # Check if filtered data is empty
    if filtered_data.empty:
        st.write("No data available for the selected city and data type.")
    else:
        # Drop rows with missing values in NO2, Latitude, or Longitude
        filtered_data = filtered_data.dropna(subset=[heatmap_column, 'Latitude', 'Longitude'])

        # Check if we have any valid data left for the heatmap
        if filtered_data.empty:
            st.write("No valid data available for the heatmap.")
        else:
            # Group by date for the selected data
            grouped_data = filtered_data.groupby('Date')

            for date, group in grouped_data:
                # Ensure that there are valid points to plot
                if not group.empty and heatmap_column in group.columns:
                    points = group[['Latitude', 'Longitude', heatmap_column]].dropna().values.tolist()
                    if points:  # Only append if points are not empty
                        heatmap_data.append(points)

            # Prepare time index
            time_index = [date.strftime('%Y-%m-%d') for date in grouped_data.groups.keys()]

            # Create Folium map centered on the selected city's average location
            if heatmap_data:
                m = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=9)

                # Create the HeatMapWithTime layer
                hm = HeatMapWithTime(heatmap_data, index=time_index, auto_play=True, max_opacity=0.6)
                hm.add_to(m)

                # Save the map to an HTML file
                m.save('NO2_HeatMapWithTime.html')

                # Display the map
                st.components.v1.html(m._repr_html_(), height=600, width=800)
            else:
                st.write("No valid points available for the heatmap.")
