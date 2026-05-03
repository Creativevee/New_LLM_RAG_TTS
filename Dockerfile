FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port (HuggingFace uses 7860)
EXPOSE 7860

# Set environment variable for HF Token (will be set in Secrets)
ENV PORT=7860

# Run the app
CMD ["python", "main.py"]