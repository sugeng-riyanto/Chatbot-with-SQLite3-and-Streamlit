import sqlite3  # Import SQLite3 to manage the database
import streamlit as st  # Import Streamlit for creating the chatbot interface
import pandas as pd  # Import Pandas for handling Excel files

# Database setup: create and populate the database
def setup_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("chatbot.db")
    cursor = connection.cursor()

    # Create a table named 'questions' if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing unique ID for each row
        question TEXT NOT NULL,                -- Column to store questions
        response TEXT NOT NULL                 -- Column to store responses
    )
    """)

    # Insert initial data into the 'questions' table
    initial_data = [
        ("What is Streamlit?", "Streamlit is an open-source app framework for Machine Learning and Data Science projects."),
        ("What is SQLite?", "SQLite is a lightweight database management system that is serverless and self-contained."),
        ("How do I install Python?", "You can install Python by downloading it from the official Python website (https://www.python.org)."),
        ("What is AI?", "AI stands for Artificial Intelligence, the simulation of human intelligence by machines."),
        ("What is the capital of France?", "The capital of France is Paris."),
    ]

    # Insert multiple rows into the table
    cursor.executemany("INSERT INTO questions (question, response) VALUES (?, ?)", initial_data)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Function to fetch response from the database
def get_response(user_question):
    connection = sqlite3.connect("chatbot.db")
    cursor = connection.cursor()
    cursor.execute("SELECT response FROM questions WHERE question LIKE ?", (f"%{user_question}%",))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else "I'm sorry, I don't have an answer for that."

# Function to add data from an uploaded Excel file
def add_data_from_excel(file):
    try:
        # Read the uploaded Excel file
        data = pd.read_excel(file)
        # Validate that the required columns exist
        if "question" in data.columns and "response" in data.columns:
            connection = sqlite3.connect("chatbot.db")
            cursor = connection.cursor()
            # Insert each row from the DataFrame into the database
            for _, row in data.iterrows():
                cursor.execute("INSERT INTO questions (question, response) VALUES (?, ?)", (row['question'], row['response']))
            connection.commit()
            connection.close()
            return "Data uploaded successfully!"
        else:
            return "Invalid file format. Please use the provided template."
    except Exception as e:
        return f"An error occurred: {e}"

# Run the setup function to initialize the database
setup_database()

# Streamlit app setup
st.title("Chatbot with SQLite3")
st.write("Ask me a question and I will try to answer based on my database!")

# User input
user_input = st.text_input("Type your question here:")

if user_input:
    response = get_response(user_input)
    st.write(f"**Bot:** {response}")

# Admin Panel
st.sidebar.title("Admin Panel")
st.sidebar.write("Add new Q&A pairs to the database.")

# Input fields for adding a new question and response
new_question = st.sidebar.text_input("Enter the question:")
new_response = st.sidebar.text_area("Enter the response:")

if st.sidebar.button("Add to Database"):
    if new_question and new_response:
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO questions (question, response) VALUES (?, ?)", (new_question, new_response))
        connection.commit()
        connection.close()
        st.sidebar.success("New Q&A added successfully!")
    else:
        st.sidebar.error("Both question and response fields are required.")

# Upload Excel file
st.sidebar.write("Or upload a spreadsheet:")
uploaded_file = st.sidebar.file_uploader("Upload Excel file (XLSX)", type=["xlsx"])

if uploaded_file:
    message = add_data_from_excel(uploaded_file)
    st.sidebar.success(message)

# Provide template for the user
st.sidebar.write("Download the template:")
template_data = pd.DataFrame({"question": ["Example question"], "response": ["Example response"]})
template_file = "template.xlsx"
template_data.to_excel(template_file, index=False)

with open(template_file, "rb") as file:
    st.sidebar.download_button("Download Template", file, file_name="template.xlsx")
