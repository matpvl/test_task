"""Contains sales app Data Transfer Object logic."""

from datetime import date
from typing import Optional

from pydantic import model_validator, Field

from src.core.common_types import BaseDTO


class DateRange(BaseDTO):
    """DTO for date range filters."""

    start_date: date = Field(
        ...,
        description="Start date in YYYY-MM-DD format",
        examples=["2023-01-01"],  # was example= now examples= with a list
    )
    end_date: date = Field(
        ...,
        description="End date in YYYY-MM-DD format",
        examples=["2023-01-31"],
    )

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRange":
        """Validate the given date range."""
        if self.end_date < self.start_date:
            error_msg = "end_date must be greater than start_date."
            raise ValueError(error_msg)
        return self


class Filters(BaseDTO):
    """DTO for filtering sales data."""

    date_range: Optional[DateRange] = Field(
        None,
        description="Optional date range filter",
        examples=[{"start_date": "2023-01-01", "end_date": "2023-01-31"}],
    )
    category: Optional[list[str]] = Field(
        None,
        description="Filter results by one or more categories",
        examples=[["Electronics", "Books"]],
    )
    product_ids: Optional[list[int]] = Field(
        None,
        description="Filter results by a list of product IDs",
        examples=[[123, 456, 789]],
    )


class SummaryRequest(BaseDTO):
    """DTO for the summary request."""

    columns: Optional[list[str]] = Field(
        default=["quantity_sold", "price_per_unit"],
        description="List of columns to compute statistics for.",
        examples=[["quantity_sold", "price_per_unit"]],
    )
    filters: Optional[Filters] = Field(
        None,
        description="Filters to apply to the sales data.",
        examples=[
            {
                "date_range": {
                    "start_date": "2023-01-01",
                    "end_date": "2023-01-31",
                },
                "category": ["Electronics"],
                "product_ids": [101, 202, 303],
            }
        ],
    )

    class Config:
        """Model configuration."""

        schema_extra = {
            "example": {
                "columns": ["quantity_sold", "price_per_unit"],
                "filters": {
                    "date_range": {
                        "start_date": "2023-01-01",
                        "end_date": "2023-01-31",
                    },
                    "category": ["Electronics"],
                    "product_ids": [101, 202, 303],
                },
            }
        }


class ColumnStatistics(BaseDTO):
    """DTO for statistics of a single column."""

    mean: float = Field(..., description="Mean of the column", examples=[125.5])
    median: float = Field(..., description="Median of the column", examples=[120.0])
    mode: float = Field(..., description="Mode of the column", examples=[115.0])
    std_dev: float = Field(
        ..., description="Standard deviation of the column", examples=[10.0]
    )
    percentile_25: float = Field(
        ..., description="25th percentile of the column", examples=[110.0]
    )
    percentile_75: float = Field(
        ..., description="75th percentile of the column", examples=[130.0]
    )

    class Config:
        """Model configuration."""

        schema_extra = {
            "example": {
                "mean": 125.5,
                "median": 120.0,
                "mode": 115.0,
                "std_dev": 10.0,
                "percentile_25": 110.0,
                "percentile_75": 130.0,
            }
        }
