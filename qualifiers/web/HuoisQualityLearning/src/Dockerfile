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
ENV FLAG=sctf{oh_no_huoi_what_have_you_done}

# Expose the port your app runs on
EXPOSE 12958

# Run the application
CMD ["python", "app.py"]
