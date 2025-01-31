# Build stage
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app

# Set working directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        qt6-base-dev \
        libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller

# Copy project files
COPY . .

# Build the application
RUN pyinstaller --name meditech_healthcheckup \
    --onefile \
    --windowed \
    --add-data "resources:resources" \
    --add-data "ui:ui" \
    main.py

# Runtime stage
FROM debian:buster-slim

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        qt6-base \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the built application
COPY --from=builder /app/dist/meditech_healthcheckup /usr/local/bin/

# Create non-root user
RUN useradd -m appuser
USER appuser

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/meditech_healthcheckup"] 