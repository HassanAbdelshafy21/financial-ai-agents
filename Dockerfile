# Use official lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY pyproject.toml poetry.lock* requirements.txt* ./

# Install dependencies (choose either poetry or pip)
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy the app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

