import matplotlib.pyplot as plt
import pandas as pd
import uvicorn
import io
from typing import Literal, Dict, Union

# FastMCP high-level server
from fastmcp import FastMCP

# Specifically import the Image helper from the utilities path to avoid ImportErrors
from fastmcp.utilities.types import Image 

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP("ChartGenerator")

@mcp.tool()
def create_chart(
    data: Dict[str, Union[int, float]], 
    chart_type: Literal["bar", "line", "pie", "area"] = "bar", 
    title: str = "Data Visualization", 
    color: str = "skyblue",
    xlabel: str = "Categories",
    ylabel: str = "Values",
    show_grid: bool = True
) -> Image:
    """
    Generates a professional chart and returns it directly to the chat without saving to disk.
    
    Args:
        data: Dictionary of labels and numeric values.
        chart_type: The visual format (bar, line, pie, or area).
        title: The chart title.
        color: CSS color name or Hex code.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        show_grid: Whether to show background grid lines.
    """
    try:
        # Convert dictionary to a pandas series for easy plotting
        df = pd.Series(data)
        
        # Create a new matplotlib figure
        plt.figure(figsize=(10, 6))
        
        # Plot based on the requested chart_type
        if chart_type == "bar":
            df.plot(kind="bar", color=color, edgecolor='black', alpha=0.8)
        elif chart_type == "line":
            df.plot(kind="line", marker='o', color=color, linewidth=2)
        elif chart_type == "area":
            df.plot(kind="area", color=color, alpha=0.4)
        elif chart_type == "pie":
            df.plot(kind="pie", autopct='%1.1f%%', startangle=140, shadow=True)
            # Pie charts do not use traditional axis labels
            ylabel, xlabel = "", ""
            
        # Add titles and axis labels
        plt.title(title, fontweight='bold')
        if xlabel: plt.xlabel(xlabel)
        if ylabel: plt.ylabel(ylabel)
        
        # Add grid lines if requested (except for pie charts)
        if show_grid and chart_type != "pie":
            plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()

        # Capture the plot in an in-memory buffer to avoid local file storage
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_bytes = buf.read()
        
        # Close the plot to free up memory
        plt.close()

        # Return a FastMCP Image object which the protocol renders in the chat
        return Image(data=img_bytes, format="png")
    
    except Exception as e:
        # Ensure resources are cleaned up on error
        plt.close()
        return f"Error generating chart: {str(e)}"

if __name__ == "__main__":
    # Use the FastMCP HTTP app to support SSE transport
    # Binding to 0.0.0.0 is required for Docker accessibility
    app = mcp.http_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)