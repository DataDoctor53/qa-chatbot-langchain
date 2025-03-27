# Use the official Python base image
FROM python:3.9-slim

# Create a working directory inside the container
WORKDIR /app

# Copy your local project files to the container’s /app directory
COPY . /app

# Install any OS-level dependencies if needed
# (Add commands like RUN apt-get update && apt-get install -y <package> if required)

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to run when the container starts
CMD ["uvicorn", "fastapiapp:app", "--host", "0.0.0.0", "--port", "8000"]
