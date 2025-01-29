FROM python:3.12.5-slim

# Working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install the needed packeges specified in the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application for development
# CMD ["python", "run.py"]

# Run the application with Gunicorn for producion
CMD ["gunicorn", "run:app", "--workers", "4", "--bind", "0.0.0.0:5000"]