FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose port
EXPOSE 8080

# Set environment variable for GCP
ENV PORT=8080

# Run the application with uvicorn (using shell form to expand PORT variable)
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
