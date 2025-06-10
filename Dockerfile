# Use a minimal Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the files into container
COPY . .

# Run the bot
CMD ["python", "main.py"]
