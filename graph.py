import traceback
import matplotlib.pyplot as plt
import pandas as pd
from agent import get_response


def generate_graph(df: pd.DataFrame, query: str):
    """Generate a graph based on user query using AI to infer the best columns."""

    # Construct LLM Prompt
    prompt = f"""
    You are an AI assistant that helps users generate graphs from a CSV file.
    The dataset contains these columns: {', '.join(df.columns)}.
    User Query: "{query}"

    1. Identify which two columns are most relevant for plotting.
    2. Suggest the best type of graph (line, bar, scatter).
    3. Only return the JSON format, nothing else:
    
    Output format:
    {{
      "x": "column_name1",
      "y": "column_name2",
      "chart_type": "line"
    }}
    """

    # Call Together API
    response = get_response(prompt)

    try:
        result = eval(response.strip())
        x_col = result.get("x")
        y_col = result.get("y")
        chart_type = result.get("chart_type", "line")

        if x_col in df.columns and y_col in df.columns:
            fig, ax = plt.subplots()
            df.plot(x=x_col, y=y_col, kind=chart_type, ax=ax)
            ax.set_title(f"{x_col} vs {y_col} ({chart_type})")
            return fig

    except Exception as e:
        print("Error processing LLM response:")
        traceback.print_exc()

    return None
