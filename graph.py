import logging
import matplotlib.pyplot as plt
import pandas as pd
from agent import get_response, get_relevant_columns


def generate_graph(df: pd.DataFrame, query: str):
    """Generate a graph based on user query using AI to infer the best columns."""
    relevant_columns = get_relevant_columns(df, query)
    # Construct LLM Prompt
    prompt = f"""
    You are an AI assistant that helps users generate graphs from a CSV file.
    The dataset: {df[relevant_columns]}.
    User Query: "{query}"

    1. Identify which two columns are most relevant for plotting.
    2. Suggest the best type of graph (line, bar, scatter).
    3. Generate list of data to be put on each axis and put it in x_data and y_data.
    4. Only return the JSON format ,with no formatting, plain text, nothing else:

    
    Output format:
    {{
      "x": "column_name1",
      "x_data":"list[]",
      "y": "column_name2",
      "y_data":"list[]",
      "chart_type": "line"
    }}
    """

    response = get_response(prompt)
    try:
        result = eval(response.strip())
        x_col = result.get("x")
        y_col = result.get("y")
        chart_type = result.get("chart_type", "line")

        x_data = result.get("x_data", [])
        y_data = result.get("y_data", [])
        chart_type = result.get("chart_type", "bar")

        fig, ax = plt.subplots()
        if not x_data or not y_data:
            if x_col in df.columns and y_col in df.columns:
                df.plot(x=x_col, y=y_col, kind=chart_type, ax=ax)
                ax.set_title(f"{x_col} vs {y_col} ({chart_type})")
                return fig
            raise ValueError("x_data and y_data cannot be empty.")

        if chart_type == "bar":
            ax.bar(x_data, y_data, color='skyblue')
        elif chart_type == "line":
            ax.plot(x_data, y_data, marker='o', linestyle='-', color='blue')
        elif chart_type == "scatter":
            ax.scatter(x_data, y_data, color='red')
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{x_col} vs {y_col} ({chart_type})")
        plt.xticks(rotation=45, ha='right')

        return fig

    except Exception as e:
        logging.error(f"Error processing:{e}")

    return None
