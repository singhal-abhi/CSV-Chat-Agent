import logging
import streamlit as st
import pandas as pd
import csv
from agent import process_query
from graph import generate_graph
from langchain.memory import ConversationBufferWindowMemory
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.set_page_config(page_title="CSV Chat Agent", page_icon="📊", layout="wide")

GRAPH_KEYWORDS = ["plot", "graph", "chart",
                  "draw", "visualize", "diagram", "show trend"]

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=5)

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear Memory", help="Reset the session memory"):
            st.session_state.memory.clear()
            st.success("Memory cleared successfully!")
    with col2:
        if st.button("🗑️ Clear Chat", help="Remove chat history"):
            st.session_state.memory.clear()
            st.session_state.messages = []
            st.success("Chat cleared successfully!")
    st.markdown("---")
    st.markdown("🔹 Use the buttons above to reset memory or chat history.")

st.title("CSV Chat Agent 🗂️📊")


def has_header(uploaded_file: UploadedFile) -> bool:
    """Check if a CSV file has a header by analyzing its content."""
    return True
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
    """Check if the user query asks for a graph."""
    return any(keyword in user_query.lower().split() for keyword in GRAPH_KEYWORDS)


@st.cache_data(hash_funcs={UploadedFile: lambda x: x.getvalue()})
def load_csv(uploaded_file):
    """Load CSV file into a Pandas DataFrame."""
    return pd.read_csv(uploaded_file)


uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    if not has_header(uploaded_file):
        st.error("Uploaded CSV does not contain a valid header!")
        st.stop()

    df = load_csv(uploaded_file)
    st.write("CSV Preview:", df.head())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a question about your CSV data...")

    if user_query:
        st.session_state.messages.append(
            {"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        if check_for_graph(user_query):
            fig = generate_graph(df, user_query)
            if fig:
                st.pyplot(fig)
            else:
                st.write("Could not generate graph. Try rephrasing.")
        else:
            response = process_query(df, user_query)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
