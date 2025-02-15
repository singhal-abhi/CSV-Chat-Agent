from langchain.memory import ConversationBufferMemory
import logging
import streamlit as st
import pandas as pd
from agent import process_query
from graph import generate_graph
import csv
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.set_page_config(
    page_title="CSV Chat Agent",
    page_icon="📊",
    layout="wide"
)
if st.button("Clear Memory 🧹", type="tertiary"):
    st.session_state.memory.clear()
    st.success("Memory cleared successfully!")

st.title("CSV Chat Agent 🗂️📊")


if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(k=8)


logging.basicConfig(level=logging.INFO)
GRAPH_KEYWORDS = ["plot", "graph", "chart",
                  "draw", "visualize", "diagram", "show trend"]


def has_header(uploaded_file: UploadedFile) -> bool:
    """Check if a CSV file has a header by analyzing its content."""
    if uploaded_file is None:
        st.error("No file uploaded.")
        return False
    try:
        uploaded_file.seek(0)
        sample = uploaded_file.read(2048).decode("utf-8")
        uploaded_file.seek(0)
        return csv.Sniffer().has_header(sample)
    except Exception as e:
        logging.error(f"Error checking header: {e}")
        st.error("An error occurred while checking the CSV header.")
        return False


def check_for_graph(user_query: str) -> bool:
    query = user_query.lower().split()
    return any(keyword in query for keyword in GRAPH_KEYWORDS)


@st.cache_data(hash_funcs={UploadedFile: lambda x: x.getvalue()})
def load_csv(uploaded_file):
    return pd.read_csv(uploaded_file)


uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    if not has_header(uploaded_file):
        st.error("Uploaded CSV does not contain a valid header!")
        st.stop()

    df = load_csv(uploaded_file)
    st.write("CSV Preview:", df.head())

    user_query = st.text_input("Ask a question about your CSV data:")

    if user_query:
        if check_for_graph(user_query):
            fig = generate_graph(df, user_query)
            if fig:
                st.pyplot(fig)
            else:
                st.write("Could not generate graph. Try rephrasing.")
        else:
            response = process_query(df, user_query)
            st.write(response)
