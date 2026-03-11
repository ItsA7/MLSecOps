# Use a standard Python computer environment
FROM python:3.9-slim

# Copy all our files into the container
COPY . /app
WORKDIR /app

# Run our script to generate the AI model
CMD ["python", "train.py"]
