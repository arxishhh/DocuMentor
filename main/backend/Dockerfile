FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt first
COPY ../../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend source code
COPY ./app ./app
COPY ./utils ./utils

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI main with uvicorn
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
