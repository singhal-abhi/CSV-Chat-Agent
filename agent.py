from typing import List
import logging
import os
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.schema import HumanMessage
import streamlit as st

llama_vision_llm = ChatOpenAI(
    # model="meta-llama/Llama-Vision-Free",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    # model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    openai_api_base="https://api.together.xyz",
    openai_api_key=os.getenv("TOGETHER_API_KEY", "default_value")
)

# This is giving better results, but has a lower token limit.
llama_instruct_llm = ChatOpenAI(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    openai_api_base="https://api.together.xyz",
    openai_api_key=os.getenv("TOGETHER_API_KEY", "default_value")
)


def get_response(prompt: str, model='instruct'):
    """Generates response using LangChain's Together API Chat Model."""
    try:
        if model == "instruct":
            response = llama_instruct_llm.invoke(
                [HumanMessage(content=prompt)])
        else:
            response = llama_vision_llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while processing your request."


def get_relevant_columns(df: pd.DataFrame, query: str) -> List:
    column_headers = ", ".join(df.columns)
    memory_context = st.session_state.memory.load_memory_variables(
        {}).get("history", "")
    prompt = f"""
    You are an AI assistant that can analyze tabular data.
    ### **Conversation History**
        {memory_context}
    
    The dataset contains the following columns:
    {column_headers}
    
    The user has asked: "{query}"
    
    Your task:
    - Identify which columns are relevant to answering the query.
    - Return only the column names which maybe useful for responding to the query.
    - Do NOT return any extra explanation, just output a Python string of relevant column names.
    
    Example output format:
    Column A,Column B,Column C
    """

    response = get_response(prompt)
    return [part.strip() for part in response.split(",") if part.strip() in column_headers]


def process_query(df: pd.DataFrame, query: str):
    """Processes user query against CSV data using LangChain & Together API."""
    selected_columns = get_relevant_columns(df, query)
    if not selected_columns:
        st.error("Unable to find relevant columns, please re-phrase the prompt.")
        st.stop()
    logging.info(f"Passing Columns {selected_columns} to the LLM")
    filtered_df = df[selected_columns].to_markdown(index=False)
    memory_context = st.session_state.memory.load_memory_variables(
        {}).get("history", "")
    prompt = f"""
        You are an AI assistant that analyzes structured CSV data to answer user queries.

        ### **Conversation History**
        {memory_context}

        ### **Dataset **
        {filtered_df} 

        ### **User Query**
        "{query}"

        ### **Instructions**
        1. **Use the conversation history** to maintain continuity in responses.
        2. **Extract data directly from the dataset**—do not assume or fabricate information.
        3. If the query asks for **numerical computations**, calculate them based on available data.
        4. If the requested information **is not found**, clearly state that it is unavailable.
        5. Be **short and precise and concise** while answering.
        6. If multiple interpretations exist, **clarify assumptions** before responding.
        7. **Do not include unrelated information or make up missing data.**
        8. Keep the answer short.

        Now, analyze the dataset and respond accurately based on the above guidelines.
    """
    response = get_response(prompt, model="vision")
    st.session_state.memory.save_context({"user": query}, {"ai": response})
    return response
