# Base image for Python environment
FROM python:3.10-slim

# Set working directory
WORKDIR /app


# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy your backend code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
