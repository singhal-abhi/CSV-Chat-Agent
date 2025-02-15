import logging
import os
import pandas as pd
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    openai_api_base="https://api.together.xyz",
    openai_api_key=os.getenv("TOGETHER_API_KEY", "default_value")
)


def get_response(prompt: str):
    """Generates response using LangChain's Together API Chat Model."""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while processing your request."


def process_query(df: pd.DataFrame, query: str):
    """Processes user query against CSV data using LangChain & Together API."""
    prompt = f"""
    You are an AI assistant that can analyze CSV data.
    Dataset being: {df}
    User Query: {query}
    Keep it easy to understand.
    """
    return get_response(prompt)
