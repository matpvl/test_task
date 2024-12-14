"""Application instance."""

from src.core.config import ApplicationConfig

app = ApplicationConfig().get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="8.0.0.0")
