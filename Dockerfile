# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. Install minimal system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install Python dependencies directly
# Note: Installing 'fastmcp' with 'uvicorn' for the HTTP transport
RUN pip install --no-cache-dir fastmcp uvicorn matplotlib pandas

# 5. Copy your adjusted server script into the container
COPY chart_server.py .

# 6. Expose the port your server will listen on
EXPOSE 8000

# 7. Run the application
CMD ["python", "chart_server.py"]