"""Project configuration file."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.core.common_types import SingletonMeta
from src.apps.sales.routers import router


class ApplicationConfig(metaclass=SingletonMeta):
    """FastAPI project configuration."""

    __slots__ = ("_asgi_app",)
    _asgi_app: FastAPI

    def __init__(self) -> None:
        """Initialize the FastAPI application."""

        self._asgi_app = FastAPI(
            title="Compstak Sales App",
            description="Sales Compstack - API Documentation",
        )
        self._asgi_app.include_router(router)

        # Mount the static files
        static_dir = Path(__file__).parent.parent / "static"
        self._asgi_app.mount(
            "/static", StaticFiles(directory=static_dir), name="static"
        )

        @self._asgi_app.get("/", response_class=HTMLResponse)
        async def read_root():
            """Return index home page."""
            index_file = static_dir / "index.html"
            return index_file.read_text(encoding="utf-8")

    def get_app(self) -> FastAPI:
        """Return FastAPI application."""

        return self._asgi_app
