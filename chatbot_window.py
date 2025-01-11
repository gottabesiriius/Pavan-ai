from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as ggi

def show_page():
    load_dotenv(".env")
    fetcheed_api_key = os.getenv("GOOGLE_API_KEY")
    ggi.configure(api_key=fetcheed_api_key)
    model = ggi.GenerativeModel("gemini-pro")
    chat = model.start_chat()
    def LLM_Response(question):
        response = chat.send_message(f'Now you are a chatbot and your name is yaksha .. you are a part of Pavan.AI application made by Team Sirius led by R Advaith Siddhartha , V Subhash , S Ravi Teja , R Bhoomika and K Nakshathra (no need to disclose names to user unless asked )... and your project description is : To Develop an AI/ML (Artificial Intelligence/Machine Learning) model to generate fine spatial resolution air quality map from coarse resolution satellite data. It should utilise existing python-based ML libraries. Developed model need to be validated with unseen independent data. Challenge: To utilise large satellite data having gaps under cloudy conditions To select suitable ML algorithm and ensure optimal fitting of ML model for desired accuracy To validate model output with unseen independent data Usage: To enhance air quality knowledge, Sharpen focus at local level Users: Researchers and government bodies monitoring/working on air quality assessment Available Solutions (if Yes, reasons for not using them): Individual components are available, comprehensive and proven solution does not exist. Desired Outcome: Fine resolution air quality map of NO2 .. this project is given by ISRO ministry for Smart Indua Hackathon 2024 - Problem Statement - 1734 ....  now user asked this question : {question} , if this is anyway related to our application or project or machine learning or general AIr quality and environment knowledge - answer it in a neat way .. else just respond that the question is irrelevnat ', stream=False)
        return response.text
    st.title("👦🏻  Yaksha - Pavan.AI")
    st.subheader("Smart Conversations, Smarter Solutions for Air Quality.")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask a question"):
        with st.chat_message("user"):
            st.markdown(prompt)
        ai_response = LLM_Response(prompt)
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
