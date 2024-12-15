FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Poetry and dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]