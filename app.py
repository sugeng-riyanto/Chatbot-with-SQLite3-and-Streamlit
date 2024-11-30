import sqlite3  # Import SQLite3 to manage the database
import streamlit as st  # Import Streamlit for creating the chatbot interface
import pandas as pd  # Import Pandas for handling Excel files

# Database setup: create and populate the database
def setup_database():
    """
    This function initializes the database and populates it with initial data.
    """
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("chatbot.db")
    cursor = connection.cursor()  # Create a cursor object to execute SQL queries

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
    """
    Fetches the best matching response from the database for a given user question.
    """
    connection = sqlite3.connect("chatbot.db")  # Connect to the database
    cursor = connection.cursor()  # Create a cursor object
    # Search for a response where the question contains the user's question
    cursor.execute("SELECT response FROM questions WHERE question LIKE ?", (f"%{user_question}%",))
    result = cursor.fetchone()  # Get the first matching result
    connection.close()  # Close the connection
    return result[0] if result else "I'm sorry, I don't have an answer for that."  # Return the result or a default message

# Function to add data from an uploaded Excel file
def add_data_from_excel(file):
    """
    Adds data from an Excel file into the database.
    """
    try:
        # Read the uploaded Excel file
        data = pd.read_excel(file)
        # Check if the required columns ('question' and 'response') exist
        if "question" in data.columns and "response" in data.columns:
            connection = sqlite3.connect("chatbot.db")  # Connect to the database
            cursor = connection.cursor()  # Create a cursor object
            # Loop through each row and insert it into the database
            for _, row in data.iterrows():
                cursor.execute("INSERT INTO questions (question, response) VALUES (?, ?)", (row['question'], row['response']))
            connection.commit()  # Commit the changes
            connection.close()  # Close the connection
            return "Data uploaded successfully!"  # Return success message
        else:
            return "Invalid file format. Please use the provided template."  # Return error if columns are missing
    except Exception as e:
        return f"An error occurred: {e}"  # Return any other errors

# Run the setup function to initialize the database
setup_database()

# Streamlit app setup
st.title("Chatbot with SQLite3")  # Set the app title
st.write("Ask me a question and I will try to answer based on my database!")  # Instructions for the user

# User input
user_input = st.text_input("Type your question here:")  # Input field for user question

if user_input:  # Check if the user has entered a question
    response = get_response(user_input)  # Get the response for the question
    st.write(f"**Bot:** {response}")  # Display the bot's response

# Admin Panel
st.sidebar.title("Admin Panel")  # Sidebar title for admin functionalities
st.sidebar.write("Add new Q&A pairs to the database.")  # Instructions for the admin

# Input fields for adding a new question and response
new_question = st.sidebar.text_input("Enter the question:")  # Field to input a new question
new_response = st.sidebar.text_area("Enter the response:")  # Field to input a new response

if st.sidebar.button("Add to Database"):  # Button to add new data to the database
    if new_question and new_response:  # Ensure both fields are filled
        connection = sqlite3.connect("chatbot.db")  # Connect to the database
        cursor = connection.cursor()  # Create a cursor object
        cursor.execute("INSERT INTO questions (question, response) VALUES (?, ?)", (new_question, new_response))  # Insert data
        connection.commit()  # Commit the changes
        connection.close()  # Close the connection
        st.sidebar.success("New Q&A added successfully!")  # Success message
    else:
        st.sidebar.error("Both question and response fields are required.")  # Error message for missing fields

# Upload Excel file
st.sidebar.write("Or upload a spreadsheet:")  # Instruction for uploading a file
uploaded_file = st.sidebar.file_uploader("Upload Excel file (XLSX)", type=["xlsx"])  # File uploader for Excel files

if uploaded_file:  # Check if a file is uploaded
    message = add_data_from_excel(uploaded_file)  # Process the uploaded file
    st.sidebar.success(message)  # Display the success or error message

# Provide template for the user
st.sidebar.write("Download the template:")  # Instruction to download the template
template_data = pd.DataFrame({"question": ["Example question"], "response": ["Example response"]})  # Example template data
template_file = "template.xlsx"  # File name for the template
template_data.to_excel(template_file, index=False)  # Save the template as an Excel file

# Button to download the template
with open(template_file, "rb") as file:
    st.sidebar.download_button("Download Template", file, file_name="template.xlsx")
