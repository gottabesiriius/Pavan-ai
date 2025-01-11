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
    # Set the page configuration
    # Title of the app
    st.image("banner.png", use_container_width=True)
    
    st.title("Interactive Air Quality Dashboard")
    
    st.markdown(
        """
        <div style="
            background-color: #f0f4fa; 
            padding: 20px; 
            border-radius: 5px; 
            margin-bottom: 25px;">
            <p style="text-align: center; color: #000000; font-size: 20px;">
                  🌱 Click anywhere on the map to instantly retrieve Latitude and Longitude values. Give it a try and explore the world in coordinates! 🌱 
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Initialize the map
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

        # Fetch data from IQAir API
        params = {"lat": lat, "lon": lng, "key": API_KEY}
        
        # Try to fetch data and handle errors
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    # Extract air quality and weather data
                    city = data["data"]["city"]
                    state = data["data"]["state"]
                    country = data["data"]["country"]
                    aqi = data['data']['current']['pollution']['aqius']
                    main_pollutant = data['data']['current']['pollution']['mainus']
                    temp = data['data']['current']['weather']['tp']
                    humidity = data['data']['current']['weather']['hu']
                    pressure = data['data']['current']['weather']['pr']
                    last_update = data['data']['current']['pollution']['ts']

                    # Display basic data
                    st.subheader(f"Air Quality in {city}, {state}, {country}")

                    # CSS for custom card layout
                    card_style = """
                    <style>
                    .card {
                        padding: 20px;
                        margin: 10px;
                        background-color: #201E43;
                        border-radius: 15px;
                        box-shadow: 
                        0px 2px 15px rgba(255,255,255, 0.5);
                        color: #333333;
                        animation: float 3s ease-in-out infinite;
                    }

                    @keyframes float {
                        0%, 100% {
                            transform: translateY(0);
                        }
                        50% {
                            transform: translateY(-10px);
                        }
                    }

                    .card h3 {
                        font-size: 1.5em;
                        margin-bottom: 10px;
                        color: #FFDA76;
                    }
                    .card p {
                        color:white;
                        font-size: 1.2em;
                        margin: 5px 0;
                    }
                    .card-container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-evenly;
                    }
                    .card-wrapper {
                        flex: 1;
                        min-width: 300px;
                        max-width: 300px;
                        margin: 10px;
                    }
                    </style>
                    """

                    # Display cards using HTML
                    card_html = f"""{card_style}
                    <div class="card-container">
                        <div class="card-wrapper">
                            <div class="card">
                                <h3>Last Updated</h3>
                                <p>{datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ')}</p>
                            </div>
                        </div>
                        <div class="card-wrapper">
                            <div class="card">
                                <h3>Air Quality Index </h3>
                                <p>{aqi}</p>
                            </div>
                        </div>
                        <div class="card-wrapper">
                            <div class="card">
                                <h3>Main Pollutant</h3>
                                <p>{main_pollutant}</p>
                            </div>
                        </div>
                        <div class="card-wrapper">
                            <div class="card">
                                <h3>Temperature</h3>
                                <p>{temp}°C</p>
                            </div>
                        </div>
                        <div class="card-wrapper">
                            <div class="card">
                                <h3>Humidity</h3>
                                <p>{humidity}%</p>
                            </div>
                        </div>
                        <div class="card-wrapper">
                            <div class="card">
                                <h3>Pressure</h3>
                                <p>{pressure} hPa</p>
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

                    # Visualizations
                    st.subheader("Visualizations")

                    # Layout with multiple columns
                    col1, col2 = st.columns(2)

                    with col1:
                        # Gauge Chart: AQI
                        aqi_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=aqi,
                            title={'text': "AQI (US)"},
                            gauge={'axis': {'range': [0, 500]},
                                'bar': {'color': "green" if aqi < 100 else "orange" if aqi < 200 else "red"}},
                        ))
                        aqi_gauge.update_layout(height=300, width=400)
                        st.plotly_chart(aqi_gauge, use_container_width=True)

                    with col2:
                        # Gauge Chart: Temperature
                        temp_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=temp,
                            title={'text': "Temperature (°C)"},
                            gauge={'axis': {'range': [-10, 50]},
                                'bar': {'color': "blue"}}
                        ))
                        temp_gauge.update_layout(height=300, width=400)
                        st.plotly_chart(temp_gauge, use_container_width=True)

                    col3, col4 = st.columns(2)

                    with col3:
                        # Gauge Chart: Humidity
                        humidity_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=humidity,
                            title={'text': "Humidity (%)"},
                            gauge={'axis': {'range': [0, 100]},
                                'bar': {'color': "purple"}}
                        ))
                        humidity_gauge.update_layout(height=300, width=400)
                        st.plotly_chart(humidity_gauge, use_container_width=True)

                    with col4:
                        # Gauge Chart: Pressure
                        pressure_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=pressure,
                            title={'text': "Pressure (hPa)"},
                            gauge={'axis': {'range': [900, 1100]},
                                'bar': {'color': "teal"}}
                        ))
                        pressure_gauge.update_layout(height=300, width=400)
                        st.plotly_chart(pressure_gauge, use_container_width=True)

                    # Simulated historical data
                    dates = pd.date_range(end=pd.Timestamp.now(), periods=30).strftime('%Y-%m-%d').tolist()
                    historical_aqi = np.random.randint(50, 300, size=30)
                    historical_temp = np.random.randint(15, 35, size=30)

                    # Line Graph: Temperature Over Time
                    st.markdown("### Temperature Over the Past 30 Days")
                    line_fig = go.Figure()
                    line_fig.add_trace(go.Scatter(
                        x=dates, y=historical_temp, mode='lines+markers', name='Temperature', line=dict(color='orange')
                    ))
                    line_fig.update_layout(title='Temperature Over Time', xaxis_title='Date', yaxis_title='Temperature (°C)', height=500)
                    st.plotly_chart(line_fig, use_container_width=True)

                    # Scatter Plot: Temperature vs AQI
                    st.markdown("### Scatter Plot: Temperature vs AQI")
                    scatter_fig = px.scatter(
                        x=historical_temp,
                        y=historical_aqi,
                        labels={'x': 'Temperature (°C)', 'y': 'AQI'},
                        title='Temperature vs AQI',
                        trendline='ols'
                    )
                    scatter_fig.update_layout(height=500)
                    st.plotly_chart(scatter_fig, use_container_width=True)
                
                    st.subheader("Visualizations")

                    # 5. Bar Chart: AQI and Humidity Over Time
                    st.markdown("### AQI and Humidity Over the Past 30 Days")
                    bar_fig = go.Figure(data=[
                        go.Bar(name='AQI', x=dates, y=historical_aqi, marker_color='indianred'),
                        go.Bar(name='Humidity', x=dates, y=[humidity]*30, marker_color='lightsalmon')
                    ])
                    bar_fig.update_layout(barmode='group', xaxis_title='Date', yaxis_title='Values', height=500)
                    st.plotly_chart(bar_fig, use_container_width=True)

                    col1, col2 = st.columns(2)

                    with col1: 
                        # 6. Pie Chart: Pollutant Breakdown (Simulated)
                        st.markdown("### Pollutant Breakdown")
                        pollutants = ['PM2.5', 'PM10', 'CO', 'O3', 'NO2']
                        pollutant_values = [40, 30, 15, 10, 5]  # Simulated values
                        pie_fig = px.pie(names=pollutants, values=pollutant_values, title='Proportion of Pollutants')
                        pie_fig.update_traces(textposition='inside', textinfo='percent+label')
                        pie_fig.update_layout(height=500)
                        st.plotly_chart(pie_fig, use_container_width=True)

                    st.header("3D Scatter Plot and 3D Surface Plot")


                    with col2 : 
                        st.markdown("### Temperature Heat Map")
                        # Simulate a 10x10 grid of temperatures
                        heat_map_data = np.random.normal(loc=temp, scale=5, size=(10, 10)).astype(int)
                        heat_map_df = pd.DataFrame(heat_map_data, columns=[f'Col {i+1}' for i in range(10)], index=[f'Row {i+1}' for i in range(10)])
                        heatmap_fig = px.imshow(heat_map_df, title='Temperature Heat Map', color_continuous_scale='Viridis')
                        heatmap_fig.update_layout(height=600)
                        st.plotly_chart(heatmap_fig, use_container_width=True)
                    # Create two columns
                    col1, col2 = st.columns(2)

                    # 3D Scatter Plot in the first column
                    with col1:
                        st.markdown("#### 3D Scatter Plot: Temperature, Humidity, AQI")
                        x = np.random.rand(50) * 40  # Temperature range from 0°C to 40°C
                        y = np.random.rand(50) * 100  # Humidity range from 0% to 100%
                        z = np.random.rand(50) * 500  # AQI range from 0 to 500

                        scatter_fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers', 
                                                                marker=dict(size=5, color=z, colorscale='Viridis'))])

                        scatter_fig.update_layout(scene=dict(xaxis_title='Temperature (°C)', 
                                                            yaxis_title='Humidity (%)', 
                                                            zaxis_title='AQI'))
                        st.plotly_chart(scatter_fig)


                    # 3D Surface Plot in the second column
                    with col2:
                        st.markdown("#### 3D Surface Plot: Simulated AQI Over Time")
                        x_surface = np.linspace(0, 29, 30)  # Simulated 30-day period
                        y_surface = np.linspace(1, 10, 10)  # Simulated 10 cities
                        x_surface, y_surface = np.meshgrid(x_surface, y_surface)
                        z_surface = np.random.rand(10, 30) * 500  # Simulated AQI values

                        surface_fig = go.Figure(data=[go.Surface(z=z_surface, x=x_surface, y=y_surface, colorscale='Rainbow')])
                        surface_fig.update_layout(scene=dict(xaxis_title='Days', 
                                                            yaxis_title='City Index', 
                                                            zaxis_title='AQI'))
                        st.plotly_chart(surface_fig)
                    col1 , col2  = st.columns(2)
                    with col1:
                        st.header("3D Line Plot: Daily AQI Trend")
                        t = np.linspace(0, 24, 100)  # Time of day in hours
                        x_line = np.linspace(0, 30, 100)  # Days
                        y_line = t
                        z_line = np.random.rand(100) * 500  # Simulated AQI

                        line_fig = go.Figure(data=[go.Scatter3d(x=x_line, y=y_line, z=z_line, mode='lines', 
                                                                line=dict(width=4, color=z_line, colorscale='Cividis'))])
                        line_fig.update_layout(scene=dict(xaxis_title='Days', 
                                                        yaxis_title='Time of Day', 
                                                        zaxis_title='AQI'))
                        st.plotly_chart(line_fig)
                    st.markdown("### Bollinger Bands for AQI")
                    bb_fig = go.Figure()

                    bb_fig.add_trace(go.Scatter(
                        x=dates, y=historical_aqi, mode='lines', name='AQI', line=dict(color='blue')
                    ))

                    # Calculate moving average and standard deviation
                    df_bb = pd.DataFrame({'Date': dates, 'AQI': historical_aqi})
                    df_bb['MA'] = df_bb['AQI'].rolling(window=5).mean()
                    df_bb['STD'] = df_bb['AQI'].rolling(window=5).std()
                    df_bb['Upper'] = df_bb['MA'] + (df_bb['STD'] * 2)
                    df_bb['Lower'] = df_bb['MA'] - (df_bb['STD'] * 2)

                    bb_fig.add_trace(go.Scatter(
                        x=df_bb['Date'], y=df_bb['Upper'], mode='lines', name='Upper Band', line=dict(color='lightblue', dash='dash')
                    ))
                    bb_fig.add_trace(go.Scatter(
                        x=df_bb['Date'], y=df_bb['Lower'], mode='lines', name='Lower Band', line=dict(color='lightblue', dash='dash'),
                        fill='tonexty', fillcolor='rgba(173,216,230,0.2)'
                    ))

                    bb_fig.update_layout(height=500, title='Bollinger Bands for AQI', xaxis_title='Date', yaxis_title='AQI')
                    st.plotly_chart(bb_fig, use_container_width=True)

                    # 10. Scatter Plot: Temperature vs AQI
                    st.markdown("### Scatter Plot: Temperature vs AQI")
                    scatter_fig = px.scatter(
                        x=historical_temp,
                        y=historical_aqi,
                        labels={'x': 'Temperature (°C)', 'y': 'AQI'},
                        title='Temperature vs AQI',
                        trendline='ols'
                    )
                    scatter_fig.update_traces(marker=dict(size=12, color='rgba(152, 0, 0, .8)', line=dict(width=2, color='DarkSlateGrey')))
                    scatter_fig.update_layout(height=500)
                    st.plotly_chart(scatter_fig, use_container_width=True)

                    # 11. Area Chart: Historical AQI
                    st.markdown("### Historical Air Quality Index Over Time (Area Chart)")
                    area_fig = go.Figure()
                    area_fig.add_trace(go.Scatter(
                        x=dates, y=historical_aqi, fill='tozeroy', name='AQI', line=dict(color='green')
                    ))
                    area_fig.update_layout(title='Historical AQI Over Time', xaxis_title='Date', yaxis_title='AQI', height=500)
                    st.plotly_chart(area_fig, use_container_width=True)

                    # 12. Map: Display AQI on Map for Selected Cities (Simulated)
                    st.markdown("### Air Quality Index Map")
                    map_data = pd.DataFrame({
                        'lat': [28.7041, 19.0760, 12.9716, 13.0827, 25.5941, 22.5726, 23.0225, 26.9124, 17.3850, 10.8505],
                        'lon': [77.1025, 72.8777, 77.5946, 80.2707, 85.1376, 88.3639, 72.5714, 75.7873, 78.4867, 76.2711],
                        'city': ["Delhi", "Mumbai", "Bangalore", "Chennai", "Lucknow", "Kolkata", "Ahmedabad", "Jaipur", "Hyderabad", "Kochi"],
                        'aqi': np.random.randint(50, 300, size=10)  # Simulated AQI values
                    })
                    map_fig = px.scatter_mapbox(
                        map_data,
                        lat="lat",
                        lon="lon",
                        hover_name="city",
                        hover_data=["aqi"],
                        color="aqi",
                        size="aqi",
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=15,
                        zoom=3
                    )
                    map_fig.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":0,"l":0,"b":0},
                        height=600,
                        title='AQI Levels in Major Indian Cities'
                    )
                    st.plotly_chart(map_fig, use_container_width=True)



                



                else:
                    st.error(f"Error: {data.get('message', 'Unable to fetch air quality data.')}")
            else:
                st.error(f"API Response Error: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"API Request Failed: {e}")
    else:
        st.write("Click on the map to get latitude and longitude.")
