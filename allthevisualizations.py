import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

def bar_chart(selected_pollutants,city_data):
    st.subheader("Bar Chart :")
    recent_data = city_data.tail(30)

    if selected_pollutants:
                fig = px.bar(
                    recent_data,
                    x=recent_data['Date'].dt.strftime('%d-%b'),
                    y=selected_pollutants,
                    barmode='group',
                    title="Pollutant Levels Over the Last 30 Days",
                    labels={'value': 'Concentration', 'Date': 'Date'},
                    height=500
                )
    st.plotly_chart(fig)

def line_chart(city_data,selected_pollutants,city):
                # Line Chart
                # Assuming `city_data` is your DataFrame and 'Date' is a datetime column.
                # Filter data for the last 2 months: 01-08-2024 to 30-09-2024
        city_data['Date'] = pd.to_datetime(city_data['Date'])  # Ensure 'Date' is in datetime format
        filtered_data = city_data[(city_data['Date'] >= '2024-08-01') & (city_data['Date'] <= '2024-09-30')]

                # Generate a sequence of dates at 5-day intervals
        desired_dates = pd.date_range(start='2024-08-01', end='2024-09-30') #freq='5D' also i can put

                # Filter the data to include only rows with dates in the 5-day sequence
        filtered_data = filtered_data[filtered_data['Date'].isin(desired_dates)]

                # Add a column for formatted dates
        filtered_data['Formatted_Date'] = filtered_data['Date'].apply(
                    lambda x: f"{x.day}{'th' if 11 <= x.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(x.day % 10, 'th')} {x.strftime('%b')}"
                )

                # Initialize Plotly figure
        fig = go.Figure()

                # Add traces for each pollutant
        for pollutant in selected_pollutants:
                    filtered_data[pollutant].fillna(method='bfill', inplace=True)  # Fill missing values
                    fig.add_trace(go.Scatter(
                        x=filtered_data['Formatted_Date'],
                        y=filtered_data[pollutant],
                        mode='lines+markers',
                        name=pollutant
                    ))

                # Update layout with transparent background
        fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                    xaxis=dict(
                        title='Date',
                        tickmode='array',
                        tickvals=filtered_data['Formatted_Date'],
                        ticktext=filtered_data['Formatted_Date'],
                        tickangle=90
                    ),
                    yaxis=dict(title='Pollutant Levels'),
                    title='Pollutant Trends (5-Day Intervals)',
                    font=dict(size=12),  # Let Plotly handle font colors dynamically
                )

                # Display the graph in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
def gauge_chart(city_data,selected_pollutants):
    # Define colour palatte
    color_palette = {
                "NO2": "red",
                "PM2.5": "orange",
                "PM10": "yellow",
                "Ozone": "blue",
                "SO2": "green",
                "CO": "purple",
                "NO": "pink",
                "NOx": "brown",
        }

        # Define gauge metrics
    gauge_metrics = {
            "NO2": (city_data['NO2'].mean(), 0, 200),
            "PM2.5": (city_data['PM2.5'].mean(), 0, 150),
            "PM10": (city_data['PM10'].mean(), 0, 250),
            "Ozone": (city_data['Ozone'].mean(), 0, 180),
            "SO2": (city_data['SO2'].mean(), 0, 100),
            "CO": (city_data['CO'].mean(), 0, 10),
            "NO": (city_data['NO'].mean(), 0, 100),
            "NOx": (city_data['NOx'].mean(), 0, 150),
        }
    max_cols = 4  

        # Total number of pollutants selected
    total_charts = len(selected_pollutants)

        # Adjust gauge chart size to fit more charts in limited space
    chart_height = 200  # Reduced height for better fit

        # Iterate through the pollutants in groups of max_cols
    for i in range(0, total_charts, max_cols):
        cols = st.columns(max_cols)  # Create exactly `max_cols` columns for each row
            
            # Iterate through pollutants in the current group
        for j, col in enumerate(cols):
                idx = i + j  # Calculate the index of the pollutant
                if idx < total_charts:
                    pollutant = selected_pollutants[idx]
                    if pollutant in gauge_metrics:
                        value, min_value, max_value = gauge_metrics[pollutant]
                        if pd.notnull(value):
                            # Create gauge chart
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=value,
                                title={'text': pollutant, 'font': {'size': 12}},  # Reduced font size
                                gauge={
                                    'axis': {'range': [min_value, max_value]},
                                    'bar': {'color': "blue"},
                                    'steps': [
                                        {'range': [min_value, max_value * 0.5], 'color': "lightgray"},
                                        {'range': [max_value * 0.5, max_value], 'color': "lightblue"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 2},  # Reduced threshold line width
                                        'thickness': 0.5,
                                        'value': value * 0.9 if value * 0.9 < max_value else max_value
                                    }
                                }
                            ))
                            # Display chart in the current column
                            col.plotly_chart(fig, use_container_width=True, height=chart_height)
                            
def pie_chart(selected_pollutants,city_data):
    if len(selected_pollutants) > 1:
                st.subheader("Pie Chart :")
                pollutant_data = city_data[selected_pollutants].mean()
                fig = px.pie(
                    values=pollutant_data,
                        names=pollutant_data.index,
                        title="Pollutant Contribution",
                        hole=0
                )
                st.plotly_chart(fig)
                
def histogram(city_data):
    st.subheader("Histogram :")
                    # Group data by Date and calculate the mean NO2 per day
    grouped_data = city_data.groupby('Date', as_index=False)['NO2'].mean()

                    # Create the histogram
    fig = px.histogram(
                        grouped_data,
                        x='Date',
                        y='NO2',
                        nbins=20,
                        title="Date vs NO2 Distribution",
                        color_discrete_sequence=['#7e3bec']  # Change color to purple
            )

                    # Update layout for better aesthetics
    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="NO2 Concentration",
                        template="plotly_white",
            )

                    # Render the histogram
    st.plotly_chart(fig)
    
def scatter_plot(selected_pollutants,city_data):
    st.subheader("3D Scatter Plot :")

    if len(selected_pollutants) >= 3:
                # Select pollutants for x, y, and z axes
            x_pollutant = st.selectbox('Select x-axis pollutant', selected_pollutants, key="x_pollutant_select")
            y_pollutant = st.selectbox('Select y-axis pollutant', selected_pollutants, key="y_pollutant_select")
            z_pollutant = st.selectbox('Select z-axis pollutant', selected_pollutants, key="z_pollutant_select")
                    
                # Convert z_pollutant to a categorical type for distinct colors
            filtered_data = city_data.dropna(subset=[x_pollutant, y_pollutant, z_pollutant])
            filtered_data[z_pollutant] = filtered_data[z_pollutant].astype(str)
                    
                # Define a qualitative color palette
            color_palette = px.colors.qualitative.Set1  # Distinct color palette
                    
                # Create the 3D scatter plot
            fig = px.scatter_3d(
                    filtered_data,
                    x=x_pollutant,
                    y=y_pollutant,
                    z=z_pollutant,
                    color=z_pollutant,  # Now z_pollutant is treated as categorical
                    color_discrete_sequence=color_palette
            )
                    
                # Render the plot
            st.plotly_chart(fig)

def no2viz():
    st.subheader("NO2 Visualization :")
    # URL of the Flask app (local or deployed)
    flask_app_url = "https://subhash.pythonanywhere.com/"  # Replace with the deployed Flask app URL if hosted

    # Center-align the iframe and make it 80% wide using custom HTML
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <iframe src="{flask_app_url}" width="120%" height="1000px" style="border:none;"></iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    