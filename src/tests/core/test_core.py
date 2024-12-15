"""Tests for project basis."""

from src.core.asgi import ApplicationConfig
from src.core.common_types import SingletonMeta


def test_application_config() -> None:
    """Test application config."""
    config = ApplicationConfig()
    app = config.get_app()
    assert app.title == "Compstac Sales App"
    assert app.description == "Sales Compstack - API Documentation"


def test_singleton_meta() -> None:
    """Test singleton allows one instance."""

    class TestClass(metaclass=SingletonMeta):
        pass

    obj1 = TestClass()
    obj2 = TestClass()
    assert obj1 is obj2
