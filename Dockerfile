FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (including docs if needed)
COPY . /app

# Set the entry point for the application (adjust if main.py has a different name)
CMD ["python", "ui.py"]
