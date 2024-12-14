"""Project configuration file."""

from fastapi import FastAPI

from src.core.routers import router
from src.core.common_types import SingletonMeta


class ApplicationConfig(metaclass=SingletonMeta):
    """FastAPI project configuration."""

    __slots__ = ("_asgi_app",)
    _asgi_app: FastAPI

    def __init__(self) -> None:
        """Initialize the FastAPI application."""

        self._asgi_app = FastAPI(
            title="Sales Compstack",
            description="Sales Compstack - API Documentation",
        )
        self._asgi_app.include_router(router)

    def get_app(self) -> FastAPI:
        """Return FastAPI application."""

        return self._asgi_app
