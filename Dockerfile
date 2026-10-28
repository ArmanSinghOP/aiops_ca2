# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and model
COPY main.py .
COPY pytest.ini .
COPY models/ ./models/
COPY tests/ ./tests/

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
