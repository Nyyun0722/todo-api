# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Set environment variable to production mode
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Default command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
