from typing import List
import logging
import os
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.schema import HumanMessage
import streamlit as st

llama_vision_llm = ChatOpenAI(
    model="meta-llama/Llama-Vision-Free",
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
            prompt += f'\nPrevious Conversations:{st.session_state.memory.load_memory_variables({}).get("chat_history", "")}'
            response = llama_vision_llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while processing your request."


def get_relevant_columns(df: pd.DataFrame, query: str) -> List:
    column_headers = ", ".join(df.columns)
    prompt = f"""
    You are an AI assistant that can analyze tabular data.
    
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

    filtered_df = df[selected_columns]
    prompt = f"""
        You are an AI assistant that analyzes structured CSV data to answer user queries.

        ### **Dataset Overview**
        - The dataset contains structured tabular data with **{len(filtered_df.columns)} columns**
        - **Dataset:** {filtered_df.to_dict(orient="records")}

        
        ### **User Query**
        "{query}"

        ### **Instructions**
        1. **Extract data directly from the dataset**—do not assume or fabricate information.
        2. If the query asks for **averages, sums, counts, or other numerical computations**, calculate them based on the provided data.
        3. If the requested information **is not found** in the dataset, **clearly state that it is unavailable** instead of making assumptions.
        4. Be **precise and concise** while answering.
        5. If multiple interpretations of the query exist, **clarify assumptions** before responding.
        6. **Do not include unrelated information or make up missing data.**
        7. Maintain the structure of the response to ensure clarity.
        8. Only provide required information, do not provide info yourself.
        Now, analyze the dataset and respond accurately based on the above guidelines.
    """
    response = get_response(prompt, model="vision")
    st.session_state.memory.save_context({"user": query}, {"ai": response})
    return response
