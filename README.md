

# Chatbot with SQLite3 and Streamlit

This project is a chatbot application built using Python, Streamlit, and SQLite3. It allows users to interact with the bot by asking questions, while admins can add new Q&A pairs manually or by uploading a spreadsheet.

---

## Features

- **User Interface:** Ask questions and get responses based on the database.
- **Admin Panel:** Add questions and responses manually or upload an Excel file.
- **Template Download:** Download a template for batch uploads.

---

## Prerequisites

1. Install Python 3.x.
2. Install the required Python packages:
   ```bash
   pip install streamlit pandas openpyxl
   ```

---

## Project Setup

### Step 1: Clone the Repository
Clone or download the project files.

### Step 2: Run the Script
Run the Streamlit application:
```bash
streamlit run chatbot_with_excel.py
```

---

## Instructions for Admins

### Add Questions Manually
1. Open the sidebar by clicking the arrow on the top-left.
2. Use the "Enter the question" and "Enter the response" fields to add new pairs.
3. Click "Add to Database" to save.

### Upload Questions via Spreadsheet
1. Use the "Download Template" button to download the Excel template.
2. Fill in your questions and responses in the appropriate columns.
3. Save the file and upload it using the "Upload Excel file" button.

---

## Template Example

| question                           | response                                      |
|------------------------------------|----------------------------------------------|
| What is Python?                    | Python is a high-level programming language. |
| What is the capital of Japan?      | The capital of Japan is Tokyo.               |

---

## For Users
1. Enter your question in the input box.
2. The chatbot will respond with the best match from its database.

---

## Contribution
Feel free to contribute by creating pull requests or raising issues for improvements.

---

## License
This project is open-source and free to use.
