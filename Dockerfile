# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Copy requirements first for better caching
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY . /code/

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application with host binding
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]