# Use official Python image
FROM python:3.12-slim

# Install application dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Copy source code
WORKDIR /app
COPY . .

# Expose port for the API
EXPOSE 8000

# Run the API service
CMD ["python", "app.py"]
