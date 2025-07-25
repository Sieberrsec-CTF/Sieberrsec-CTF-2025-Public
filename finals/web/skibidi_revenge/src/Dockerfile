# Use the latest Python image
FROM python:latest

# Set working directory
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (adjust if your app uses a different port)
EXPOSE 5000

# Run the async application
CMD ["python", "app.py"]