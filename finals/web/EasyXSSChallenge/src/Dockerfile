# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update 
RUN apt install --no-install-recommends -y chromium

# Copy the application code
COPY . .
RUN mkdir templates/user_templates

# Set environment variables
ENV FLAG=sctf{i_l0v3_xss_ch4ll3ng3s}

# Expose the port your app runs on
EXPOSE 38457

# Run the application
CMD ["python", "app.py"]
