"""Contains sales app Data Transfer Object logic."""

from datetime import date
from typing import Optional

from src.core.common_types import BaseDTO


class DateRange(BaseDTO):
    """DTO for date range filters."""

    start_date: date
    """ISO format (YYYY-MM-DD)"""
    end_date: date
    """ISO format (YYYY-MM-DD)"""

    # TODO Matija: validator for end_date > start_date


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

    mean: Optional[float]
    median: Optional[float]
    mode: Optional[float]
    std_dev: Optional[float]
    percentile_25: Optional[float]
    percentile_75: Optional[float]


class SummaryResponse(BaseDTO):
    """DTO for the summary response."""

    root_model: dict[str, ColumnStatistics]
