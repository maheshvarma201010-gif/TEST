FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose health check port
EXPOSE 8000

# Run the application
CMD ["python3", "bot.py"]
