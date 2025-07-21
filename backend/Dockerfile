# Use official Python image
FROM python:3.12-slim

# Install application dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy source code
WORKDIR /app
COPY . .

# Expose port for the API
EXPOSE 8000

# Run the API service
CMD ["python", "app.py"]
