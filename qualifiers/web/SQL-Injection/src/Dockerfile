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
ENV FLAG=sctf{c0ngr4tulat10ns_0n_y0ur_f1rst_sql_injection}

# Expose the port your app runs on
EXPOSE 12085

# Run the application
CMD ["python", "app.py"]
