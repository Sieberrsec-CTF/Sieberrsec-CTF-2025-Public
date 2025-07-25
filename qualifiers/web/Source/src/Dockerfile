# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV FLAG=sctf{chrome_devtools_are_really_useful}

# Expose the port your app runs on
EXPOSE 18537

# Run the application
CMD ["python", "app.py"]
