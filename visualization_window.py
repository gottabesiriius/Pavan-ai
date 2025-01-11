import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from heatmaptime import heatmap_timebased
from streamlit_folium import st_folium
from globee import calling_globe
from allthevisualizations import line_chart,bar_chart,pie_chart,gauge_chart,histogram,scatter_plot
import random
import base64

def show_page():
    # Function to load and encode image as base64
# --------------------------------------------------------- data loading and cleaning ---------------------------------------------------
    GROUND_DATA_PATH = "ground_data2.csv"
    SATELLITE_DATA_PATH = "modified_satellite_data2.csv"

    # Load and clean data function
    def load_and_clean_data(data_path):
        try:
            # Load data
            data = pd.read_csv(data_path)

            # Ensure 'Date' column is properly formatted
            data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y %H:%M', errors='coerce')

            # Convert pollutant columns to numeric, except for non-numeric ones
            for col in data.columns:
                if col not in ['Date', 'City', 'Location', 'Latitude', 'Longitude']:
                    data[col] = pd.to_numeric(data[col], errors='coerce')

            # Clean Latitude and Longitude columns
            data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
            data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')

            # Remove rows with invalid Latitude/Longitude or Date
            data = data.dropna(subset=['Latitude', 'Longitude', 'Date'])

            return data
        except Exception as e:
            st.error(f"Error loading or cleaning data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    # Load both datasets (Ground and Satellite)
    ground_data = load_and_clean_data(GROUND_DATA_PATH)
    satellite_data = load_and_clean_data(SATELLITE_DATA_PATH)

# ------------------------------------------------------- User interaction ---------------------------------------------------------------------

    # Sidebar Filters
    st.image("banner.png", use_container_width=True)
    
    
    st.title("Data Visualization Hub")
    st.markdown(
        """
        <div style="
            background-color: #f0f4fa; 
            padding: 20px; 
            border-radius: 5px; 
            margin-bottom: 25px;">
            <p style="text-align: center; color: #000000; font-size: 20px;">
                ✨ This page provides an interactive way to analyze air quality trends. Explore the data and uncover insights! 📊
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    city = st.selectbox('Select City', ground_data['City'].unique(), key="city_select")
    data_type = st.radio("Select Type of Data for Visualization :", ['Ground Data', 'Satellite Data'], key="heatmap_data_type")

    # Filter city data based on user selection
    if data_type == 'Ground Data':
        city_data = ground_data[ground_data['City'] == city]
        ground_data_vizz=city_data
        
    elif data_type == 'Satellite Data':
        city_data = satellite_data[satellite_data['City'] == city]

    # Pollutants filter (automatically populate based on columns)
    pollutants = [col for col in city_data.columns if col not in ['Date', 'City', 'Location', 'Latitude', 'Longitude']]
    selected_pollutants = st.multiselect('Select Pollutants', pollutants, key="pollutant_select")

    col1, col2 = st.columns([2, 1.4])

    with col1:
        # Time-based Heatmap
        heatmap_timebased(city,data_type)

    with col2:
        # Generate points data with random AQI values and unique colors
        st.subheader("3D Visualization :")
        if data_type:
            calling_globe()

    # -----------------------------------------------------------------      VISUALIZATIONS      -------------------------------------------------------------------------------------------

    col3, col4 = st.columns([2, 1])

    # Air quality chart
    if data_type=="Ground Data":
        if selected_pollutants:
            with col3:
                st.subheader(f"Air Quality Analysis in {city} : ")
                if not city_data['Date'].isnull().all():
                    year = city_data['Date'].dt.year.unique()[0]
                    st.markdown(f"**Year:** {year}")

                    # Line Chart
                    # Assuming `city_data` is your DataFrame and 'Date' is a datetime column.
                    # Filter data for the last 2 months: 01-08-2024 to 30-09-2024
                    line_chart(ground_data_vizz,selected_pollutants,city)

        # Assuming `city_data` and `selected_pollutants` are already defined
            col5, col6 = st.columns([2, 2])

            st.subheader("Gauge Charts: Pollutant Levels")
            gauge_chart(ground_data_vizz,selected_pollutants)
            
            # Bar Chart
            with col4:
                bar_chart(selected_pollutants,ground_data_vizz)
                    
            # Pie Chart
            with col5:
                pie_chart(selected_pollutants,ground_data_vizz)
            
            with col6:   
                histogram(ground_data_vizz)

            #3D Scatter Plot
            scatter_plot(selected_pollutants,city_data)

    if data_type=="Satellite Data":
        if selected_pollutants:
            with col3:
                st.subheader(f"Air Quality Analysis in {city} :")
                if not city_data['Date'].isnull().all():
                    year = city_data['Date'].dt.year.unique()[0]
                    st.markdown(f"**Year:** {year}")

                    # Line Chart
                    # Assuming `city_data` is your DataFrame and 'Date' is a datetime column.
                    # Filter data for the last 2 months: 01-08-2024 to 30-09-2024
                    line_chart(ground_data_vizz,selected_pollutants,city)

        # Assuming `city_data` and `selected_pollutants` are already defined
            col5, col6 = st.columns([2, 2])

            st.subheader("Gauge Charts: Pollutant Levels")
            gauge_chart(ground_data_vizz,selected_pollutants)
            
            # Bar Chart
            with col4:
                bar_chart(selected_pollutants,ground_data_vizz)
                    
            # Pie Chart
            with col5:
                pie_chart(selected_pollutants,ground_data_vizz)
            
            with col6:   
                histogram(ground_data_vizz)

            #3D Scatter Plot
            scatter_plot(selected_pollutants,city_data)