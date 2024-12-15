"""Contains sales app Data Transfer Object logic."""

from datetime import date
from typing import Optional

from pydantic import model_validator

from src.core.common_types import BaseDTO


class DateRange(BaseDTO):
    """DTO for date range filters."""

    start_date: date
    """ISO format (YYYY-MM-DD)"""
    end_date: date
    """ISO format (YYYY-MM-DD)"""

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRange":
        """Validate the given date range."""

        if self.end_date < self.start_date:
            error = "end_date must be greater than start_date."
            raise ValueError(error)
        return self


class Filters(BaseDTO):
    """DTO for filtering sales data."""

    date_range: Optional[DateRange] = None
    category: Optional[list[str]] = None
    product_ids: Optional[list[int]] = None


class SummaryRequest(BaseDTO):
    """DTO for the summary request."""

    columns: Optional[list[str]] = ["quantity_sold", "price_per_unit"]
    filters: Optional[Filters] = None


class ColumnStatistics(BaseDTO):
    """DTO for statistics of a single column."""

    mean: float
    median: float
    mode: float
    std_dev: float
    percentile_25: float
    percentile_75: float
