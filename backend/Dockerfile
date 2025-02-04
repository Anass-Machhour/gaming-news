FROM python:3.12.5-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements file first
COPY requirements.txt .

# Install dependencies as root
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user
RUN useradd -m appuser

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]