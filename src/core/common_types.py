"""Common types used across the project."""

from typing import Any, ClassVar
from pydantic import BaseModel, ConfigDict


class SingletonMeta(type):
    """Singleton base metaclass."""

    _instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "SingletonMeta":
        """Instantiate a Singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseDTO(BaseModel):
    """Base data transfer object."""

    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )
