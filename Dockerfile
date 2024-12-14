FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# install curl to check debug connection between containers
# after apt-get update and curl installation we remove the excess packages
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.app.api:app", "--host", "0.0.0.0"]