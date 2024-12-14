"""Tests for models (data transfer objects)."""

import pytest
from pydantic import ValidationError

from src.apps.sales.dto import DateRange, Filters, SummaryRequest
from src.tests.const import Some


def test_date_range_converts_string() -> None:
    """Test date range returns a date."""

    date_range = DateRange(start_date="2023-01-01", end_date="2023-01-31")  # type: ignore[arg-type]
    assert date_range.start_date == Some.VALID_START_DATE
    assert date_range.end_date == Some.VALID_END_DATE


def test_filters_valid() -> None:
    """Test valid Filters DTO."""
    filters = Filters(
        date_range=DateRange(
            start_date=Some.VALID_START_DATE, end_date=Some.VALID_END_DATE
        ),
        category=["Electronics", "Clothing"],
        product_ids=[1001, 1002],
    )

    expected_product_value = 1001

    assert filters.date_range is not None
    assert filters.date_range.start_date is not None
    assert filters.category is not None
    assert filters.product_ids is not None
    assert filters.date_range.start_date == "2023-01-01"
    assert "Electronics" in filters.category
    assert expected_product_value in filters.product_ids


def test_filters_optional_fields() -> None:
    """Test Filters DTO's fields are optional."""
    filters = Filters()
    assert filters.date_range is None
    assert filters.category is None
    assert filters.product_ids is None


def test_summary_request_valid() -> None:
    """Test valid SummaryRequest DTO."""
    request = SummaryRequest(
        columns=["quantity_sold"],
        filters=Filters(
            date_range=DateRange(
                start_date=Some.VALID_START_DATE, end_date=Some.VALID_END_DATE
            ),
            category=["Electronics"],
            product_ids=[1001],
        ),
    )
    assert request.filters is not None
    assert request.filters.date_range is not None
    assert request.filters.date_range.start_date is not None
    assert request.columns == ["quantity_sold"]
    assert request.filters.date_range.start_date == "2023-01-01"


def test_summary_request_defaults() -> None:
    """Test SummaryRequest DTO with default values."""
    request = SummaryRequest()
    assert request.columns == ["quantity_sold", "price_per_unit"]
    assert request.filters is None


def test_summary_request_invalid_columns() -> None:
    """Test SummaryRequest DTO with invalid type for columns."""
    with pytest.raises(ValidationError):
        SummaryRequest(columns=123)  # type: ignore[arg-type]
