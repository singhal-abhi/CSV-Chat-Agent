# CSV Chat Agent

## Overview
CSV Chat Agent is an interactive web application that enables users to upload CSV files, validate their contents, and interact with the data using natural language. The application can also generate graphs when users request visualizations.

## Features
✅ **CSV Upload & Validation** – Ensures the uploaded file is a valid CSV with headers.  
✅ **Chat with Data** – Uses an LLM to process natural language queries and extract insights from the CSV.  
✅ **Graph Generation** – Automatically creates visualizations based on user queries.  
✅ **User-Friendly Web Interface** – Built with Streamlit for an intuitive and responsive experience.  

## Tech Stack
- **Python** – Core programming language.  
- **Streamlit** – Web framework for UI.  
- **LangChain** – LLM-powered query processing.  
- **Together API** – Handles natural language understanding.  
- **Matplotlib & Plotly** – Generates data visualizations.  
- **Pandas** – Processes CSV data.  

## Installation

### Prerequisites
Ensure you have Python **3.8 or later** installed.

### Setup Instructions

1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/your-repo/csv-chat-agent.git
cd csv-chat-agent
```

2️⃣ **Install Dependencies**  
```sh
pip install -r requirements.txt
```

3️⃣ **Set Up API Key**  
Obtain a Together API key from [Together AI](https://www.together.xyz) and set it as an environment variable:  

- **Linux/Mac:**  
  ```sh
  export TOGETHER_API_KEY="your-api-key"
  ```  
- **Windows (Command Prompt):**  
  ```sh
  set TOGETHER_API_KEY="your-api-key"
  ```  

4️⃣ **Run the Application**  
```sh
streamlit run app.py
```

## Usage
1. Open your browser and go to the URL provided by Streamlit.  
2. Upload a CSV file using the file uploader.  
3. Enter a natural language query to interact with the data.  
4. If requested, the system will generate and display relevant graphs.  

## Contact
For any questions or feedback, please reach out at: **your-email@example.com**  
