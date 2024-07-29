import streamlit as st 
from pandasai.llm.openai import OpenAI
import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser
import matplotlib.pyplot as plt
import io


openai_api_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai_api_key)

st.set_page_config(layout='wide')

st.title("Genie🤓")

# Catchy description
st.markdown("""
**Welcome to Genie🤓!**

**Your Intelligent Data Whisperer:**
Upload your CSV files, ask insightful questions, and get instant answers. Whether it's generating interactive visualizations, performing data analysis, or simply making sense of your data, our AI-powered chatbot is here to assist. Transform your raw data into meaningful insights effortlessly. Let Data Analytics Buddy take your data exploration to the next level!
""")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1').fillna(value=0)
    st.write("Uploaded CSV file:")
    st.write(df)
    
    llm = OpenAI(api_token=openai_api_key)
    query_engine = SmartDataframe(df,config={"llm": llm,"response_parser": ResponseParser})
    # Add a text input for user queries
    user_query = st.text_input("Ask a question about your data:")
    if user_query:
        #Invoke the agent with the human message and display the output
        response = query_engine.chat(user_query)
        st.write("Genie🤓:")
        st.write(response)

         # Check if the response includes a plot
        if "plot" in response:
            # Capture the plot by saving it to a buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
    
            # Display the plot
            st.pyplot(plt)
    
            # Clear the plot to avoid overlapping plots
            plt.clf()

else:
    st.write("Please upload a CSV file to proceed.")
