FROM python:3.12-slim AS base

# Set working directory
WORKDIR /app

# Environment settings for better Docker behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM base AS final
WORKDIR /app

# Copy the rest of the source code
COPY . .

# Expose the app port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
