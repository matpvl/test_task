"""Tests for models (data transfer objects)."""

import pytest
import pandas as pd
from pydantic import ValidationError

from src.apps.sales.dto import (
    DateRange,
    Filters,
    SummaryRequest,
    ColumnStatistics,
)
from src.tests.const import Some


@pytest.fixture
def mock_load_data(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture to mock the load_data function."""

    def _mock_load_data() -> pd.DataFrame:
        # Return a DataFrame with the necessary columns and valid categories
        return pd.DataFrame(
            {
                "category": ["Electronics", "Clothing"],
                "date": ["2023-01-01", "2023-01-15"],
                "product_id": [1001, 1002],
                "quantity_sold": [10, 20],
                "price_per_unit": [5.0, 15.0],
            }
        )

    # Apply the monkeypatch to replace load_data with the mock
    monkeypatch.setattr("src.apps.sales.data_utils.load_data", _mock_load_data)


def test_date_range_converts_string() -> None:
    """Test date range returns a date."""

    date_range = DateRange(start_date="2023-01-01", end_date="2023-01-31")  # type: ignore[arg-type]
    assert date_range.start_date == Some.START_DATE
    assert date_range.end_date == Some.END_DATE


def test_filters_valid(mock_load_data: pytest.MonkeyPatch) -> None:  # noqa:ARG001
    """Test valid Filters DTO."""
    filters = Filters(
        date_range=DateRange(
            start_date="2023-01-01",  # type: ignore[arg-type]
            end_date=Some.END_DATE,
        ),
        category=["Electronics", "Clothing"],
        product_ids=[1001, 1002],
    )

    expected_product_value = 1001

    assert filters.date_range is not None
    assert filters.date_range.start_date is not None
    assert filters.category is not None
    assert filters.product_ids is not None
    assert filters.date_range.start_date == Some.START_DATE
    assert "Electronics" in filters.category
    assert expected_product_value in filters.product_ids


def test_filters_optional_fields() -> None:
    """Test Filters DTO's fields are optional."""
    filters = Filters()  # type: ignore[call-arg]
    assert filters.date_range is None
    assert filters.category is None
    assert filters.product_ids is None


def test_summary_request_valid(
    mock_load_data: pytest.MonkeyPatch,  # noqa:ARG001
) -> None:
    """Test valid SummaryRequest DTO."""
    request = SummaryRequest(
        columns=["quantity_sold"],
        filters=Filters(
            date_range=DateRange(start_date=Some.START_DATE, end_date=Some.END_DATE),
            category=["Electronics"],
            product_ids=[1001],
        ),
    )
    assert request.filters is not None
    assert request.filters.date_range is not None
    assert request.filters.date_range.start_date is not None
    assert request.columns == ["quantity_sold"]
    assert request.filters.date_range.start_date == Some.START_DATE


def test_summary_request_defaults() -> None:
    """Test SummaryRequest DTO with default values."""
    request = SummaryRequest()  # type: ignore[call-arg]
    assert request.columns == ["quantity_sold", "price_per_unit"]
    assert request.filters is None


def test_summary_request_invalid_columns() -> None:
    """Test SummaryRequest DTO with invalid type for columns."""
    with pytest.raises(ValidationError):
        SummaryRequest(columns=123)  # type: ignore[arg-type, call-arg]


def test_column_statistics_valid() -> None:
    """Test valid ColumnStatistics DTO."""
    expected_mean = 15.2
    expected_median = 10
    expected_mode = 8
    expected_std_dev = 5.6
    expected_percentile_25 = 7
    expected_percentile_75 = 20

    stats = ColumnStatistics(
        mean=expected_mean,
        median=expected_median,
        mode=expected_mode,
        std_dev=expected_std_dev,
        percentile_25=expected_percentile_25,
        percentile_75=expected_percentile_75,
    )

    assert stats.mean == expected_mean
    assert stats.median == expected_median
    assert stats.mode == expected_mode
    assert stats.std_dev == expected_std_dev
    assert stats.percentile_25 == expected_percentile_25
    assert stats.percentile_75 == expected_percentile_75


def test_column_statistics_invalid_type() -> None:
    """Test ColumnStatistics DTO with invalid field types."""

    with pytest.raises(ValidationError):
        ColumnStatistics(mean="invalid")  # type: ignore[call-arg, arg-type]


def test_date_range_invalid_order() -> None:
    """Test DateRange with end_date earlier than start_date."""
    with pytest.raises(
        ValidationError, match="end_date must be greater than start_date."
    ):
        DateRange(start_date="2023-01-31", end_date="2023-01-01")  # type: ignore[arg-type]


def test_date_range_missing_end_date() -> None:
    """Test DateRange when end_date is missing."""
    with pytest.raises(ValidationError, match=r"end_date\s+Field required"):
        DateRange(start_date="2023-01-01")  # type: ignore[call-arg, arg-type]
