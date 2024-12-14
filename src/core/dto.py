"""File containing base DTO."""

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """Base data transfer object."""

    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )
