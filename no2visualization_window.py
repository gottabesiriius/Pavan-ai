import streamlit as st

def show_page():
    # Title of the Streamlit app
    st.image("banner.png", use_container_width=True)
    st.title("NO2 Insights")
    
    st.markdown(
        """
        <div style="
            background-color: #f0f4fa; 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 20px;">
            <p style="text-align: center; color: #000000; font-size: 20px;">
                📉 Get all the NO2 Insights here and explore it's levels across various cities in India! 🌟
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Instructions
    st.markdown("""
    🟡 Note : This is a Streamlit app embedding a Flask app using an iframe.
    The Flask app runs locally or on a server and is displayed below.
    """)

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