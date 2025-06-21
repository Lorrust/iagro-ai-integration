FROM python:3.12.5-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependencies first
COPY pyproject.toml poetry.lock ./

# Install dependencies (system + Python)
RUN apt-get update && apt-get install -y build-essential && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Default command can be overridden in docker-compose
CMD ["poetry", "run", "start"]
