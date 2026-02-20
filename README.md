# ChartGenerator MCP Server

This project is a Model Context Protocol (MCP) server that provides professional data visualization tools for AI assistants like Cursor. It uses **FastMCP** and **Matplotlib** to generate various types of charts (bar, line, pie, and area) and saves them directly to a local directory.

## Features

* **Multi-Type Charting**: Supports bar, line, area, and pie charts.
* **Customizable Styling**: Adjust titles, colors, axis labels, and grid visibility through tool parameters.
* **Automated Saving**: Automatically generates unique filenames using timestamps and saves charts to a designated output folder.
* **FastMCP Integration**: Built on the FastMCP framework for high-performance tool execution.

## Prerequisites

Before running the server, ensure you have the following Python packages installed:

```bash
pip install fastmcp uvicorn matplotlib pandas

```

## Program Structure

The core logic is contained in `chart_server.py`, which performs the following steps:

1. **Initializes FastMCP**: Creates a server named `ChartGenerator`.
2. **Environment Setup**: Ensures the `/app/output` directory exists for storing generated images.
3. **Tool Definition**: Exposes the `create_chart` tool with the following parameters:
* `data`: A dictionary of labels and numeric values.
* `chart_type`: Options include `bar`, `line`, `pie`, or `area`.
* `title`: The title displayed at the top of the chart.
* `color`: The primary color for the data visualization.
* `xlabel` / `ylabel`: Labels for the horizontal and vertical axes.
* `show_grid`: Boolean to toggle the background grid (disabled automatically for pie charts).


4. **Execution**: Starts an ASGI application using `uvicorn` on `host 0.0.0.0` and `port 8000`.

## How to Run

1. **Direct Execution**:
```bash
python chart_server.py

```


2. **Docker Execution** (Recommended for the current setup):
If using Docker, ensure your volume is mapped to `D:\2026\graphics\charts` to match the program's return message.

## Usage Example (Cursor Prompt)

Once the server is connected to Cursor, you can ask:

> "Use ChartMaker to create a **bar chart** with this data: {'Jan': 45, 'Feb': 52, 'Mar': 38}. Set the color to 'skyblue' and title it 'Q1 Sales Performance'."

## Error Handling

The program includes a `try-except` block that captures exceptions during chart generation. If an error occurs, the server will close the current plot to free resources and return the error message as a string.