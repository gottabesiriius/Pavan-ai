import streamlit as st

# Set page configuration
def show_page():

    # Title and subtitle
    # Image banner or background
    st.image("banner.png", use_container_width=True, caption="Empowering Air Quality Monitoring")
    
    st.markdown(
        """
        <div style="
            background-color: #f0f4fa; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 25px;">
            <h2 style="text-align: center; color: #4A90E2;">
                Explore, Analyze, and Predict Air Quality Data
            </h2>
            <p style="text-align: center; color: #000000; font-size: 16px;">
                🌍 Dive into interactive visualizations, insightful trends, and cutting-edge predictions 
                powered by ISRO's NO<sub>2</sub> data. 📈
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Navigation buttons to different pages
    st.subheader("PAVAN.AI ")
    st.write("An ML model that generates fine spatial resolution air quality maps from coarse resolution satellite data.")
    
    st.markdown("### Explore Features of Pavan AI ✨")
    st.write("📊 Visualization Hub - Interactive charts and heatmaps to analyze NO₂ data trends. ")
    st.write("🤖 Prediction Models - Accurately forecast NO₂ levels using advanced machine learning models. ")
    st.write("📍 Latitude and longitude - Retrieve air quality data for any location with precise coordinates. ")
    st.write("🔍 Find Nearest Station - Locate the closest air quality monitoring station instantly. ")
    st.write("💬 Yaksha - Get quick answers to your air quality questions with our smart chatbot. ")
    st.write("🔎 NO2 Insights - In-depth analysis and trends of NO₂ levels across regions. ")
    st.write("🌱 NDVI - Know the NDVI, Elevation and Population Density. ")

    st.write(" Enjoy exploring! ")
    # Additional info or footer
    st.markdown("---")
    st.markdown(
        """
        <footer style="text-align: center; font-size: 12px; color: #aaa;">
            Built by Team Sirius | Powered by ISRO's NO<sub>2</sub> Data
        </footer>
        """, 
        unsafe_allow_html=True
    )