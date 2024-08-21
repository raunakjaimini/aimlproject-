from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Google Gemini model
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {e}"

# Function to retrieve data from the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        return f"SQL error: {e}"

# Define your prompt for the LLM
prompt = [
    """
    You are an expert in converting English questions to SQL queries.
    The SQL database is named analytics and the table name is tablee and has the following columns:
    - PAGE TITLE AND SCREEN NAME
    - COUNTRY
    - VIEWS
    - USERS
    - VIEWS PER USER
    - AVERAGE ENGAGEMENT TIME
    - EVENT COUNT
    - KEY EVENTS
    Convert the given English question into a valid SQL query to retrieve data from this database.
    """
]

# Streamlit app setup
st.set_page_config(page_title="SQL Query Retriever")
st.header("Gemini App to Retrieve SQL Data")

question = st.text_input("Enter your question:", key="input")
submit = st.button("Submit")

if submit:
    if question:
        with st.spinner("Generating SQL query..."):
            sql_query = get_gemini_response(question, prompt)
        
        # Clean up SQL query string to remove markdown syntax and unwanted characters
        sql_query = sql_query.replace('sql', '').replace('', '').strip()
        
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language='sql')
        
        with st.spinner("Fetching data from the database..."):
            result = read_sql_query(sql_query, "analytics.db")
            
        if isinstance(result, str):  # Error message from SQL operation
            st.error(result)
        else:
            st.subheader("Query Result:")
            if result:
                # Get the column names from the database
                conn = sqlite3.connect("analytics.db")
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(tablee);")
                columns = [desc[1] for desc in cursor.fetchall()]
                conn.close()
                
                # Display results in a table format
                df = pd.DataFrame(result, columns=columns)
                st.write(df)
            else:
                st.write("No results found.")
    else:
        st.warning("Please enter a question.")