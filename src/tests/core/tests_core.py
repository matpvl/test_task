"""Tests for project basis."""

from src.core.common_types import SingletonMeta
from src.core.config import ApplicationConfig


def test_application_config() -> None:
    """Test application config."""
    config = ApplicationConfig()
    app = config.get_app()
    assert app.title == "Sales Compstack"
    assert app.description == "Sales Compstack - API Documentation"


def test_singleton_meta() -> None:
    """Test singleton allows one instance."""

    class TestClass(metaclass=SingletonMeta):
        pass

    obj1 = TestClass()
    obj2 = TestClass()
    assert obj1 is obj2
