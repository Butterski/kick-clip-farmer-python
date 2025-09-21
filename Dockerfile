# Use Python 3.11 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py main_no_proxy.py ./
COPY proxies.txt ./

# Create a non-root user for security
RUN useradd -m -u 1000 kickbot && chown -R kickbot:kickbot /app
USER kickbot

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command (can be overridden)
CMD ["python", "main.py"]