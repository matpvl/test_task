FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VERSION=1.6.1
RUN pip install --no-cache-dir poetry=="${POETRY_VERSION}"

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.core.asgi:app", "--host", "0.0.0.0", "--port", "8000"]