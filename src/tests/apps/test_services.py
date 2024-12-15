"""Tests for the sales app business logic."""

from pathlib import Path

import pandas as pd
import pytest

from src.apps.sales.dto import Filters, DateRange
from src.apps.sales.services import load_data, filter_data, compute_statistics
from src.core.settings import settings
from src.tests.const import Some


@pytest.fixture
def mock_data() -> pd.DataFrame:
    """Fixture to provide mock sales data for testing."""
    return pd.DataFrame(
        {
            "date": ["2023-01-01", "2023-01-15", "2023-01-20", "2023-02-01"],
            "product_id": [1001, 1002, 1003, 1004],
            "category": ["Electronics", "Clothing", "Electronics", "Clothing"],
            "quantity_sold": [10, 20, 30, 40],
            "price_per_unit": [5.0, 15.0, 25.0, 35.0],
        }
    )


def test_load_data_valid(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test loading a valid sales data file."""

    # we mock a valid CSV file
    csv_content = """date,product_id,category,quantity_sold,price_per_unit
                    2023-01-01,1001,Electronics,10,5.0
                    2023-01-15,1002,Clothing,20,15.0
                    """

    file_path = tmp_path / "sales_data.csv"
    file_path.write_text(csv_content)

    # Monkeypatch settings to point to the mock file
    monkeypatch.setattr(settings, "sales_data", file_path)

    data = load_data()

    expected_product_id = 1001
    expected_data_len = 2

    # Assertions
    assert isinstance(data, pd.DataFrame)
    assert len(data) == expected_data_len
    assert data.iloc[0]["product_id"] == expected_product_id


def test_load_data_file_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test behavior when the sales data file is not found."""

    file_path = Path("totally/non/existent/file_path")
    monkeypatch.setattr(settings, "sales_data", file_path)

    with pytest.raises(FileNotFoundError, match="Sales data file not found"):
        load_data()


def test_load_data_empty_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test behavior when the sales data file is empty."""

    file_path = tmp_path / "sales_data.csv"

    # create an empty file for the test case
    file_path.touch()

    monkeypatch.setattr(settings, "sales_data", file_path)

    # Assert the function raises ValueError
    with pytest.raises(ValueError, match="Sales data file is empty"):
        load_data()


def test_load_data_invalid_csv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test behavior when the sales data file is invalid."""

    invalid_content = """invalid content, not a CSV"""
    file_path = tmp_path / "sales_data.csv"
    file_path.write_text(invalid_content)

    # Monkeypatch settings to point to the mock file
    monkeypatch.setattr(settings, "sales_data", file_path)

    # Assert the function raises ValueError
    with pytest.raises(
        ValueError,
        match="Sales data file does not contain the required columns",
    ):
        load_data()


def test_filter_data_no_filters(mock_data: pd.DataFrame) -> None:
    """Test filter_data with no filters applied."""

    filtered_data = filter_data(mock_data, None)
    assert len(filtered_data) == len(mock_data)
    pd.testing.assert_frame_equal(filtered_data, mock_data)


def test_filter_data_date_range(mock_data: pd.DataFrame) -> None:
    """Test filter_data with a date range filter."""

    filters = Filters(  # type: ignore[call-arg]
        date_range=DateRange(
            start_date=Some.START_DATE, end_date=Some.END_DATE_2
        )
    )
    filtered_data = filter_data(mock_data, filters)

    expected_data_len = 2
    assert len(filtered_data) == expected_data_len
    assert all(filtered_data["date"].between("2023-01-01", "2023-01-15"))


def test_filter_data_future_end_date(mock_data: pd.DataFrame) -> None:
    """Test filter_data with a future end date returns all dates smaller than it."""

    filters = Filters(  # type: ignore[call-arg]
        date_range=DateRange(
            start_date=Some.START_DATE, end_date=Some.FUTURE_DATE
        )
    )
    filtered_data = filter_data(mock_data, filters)

    expected_data_len = 4
    assert len(filtered_data) == expected_data_len


def test_filter_data_category(mock_data: pd.DataFrame) -> None:
    """Test filter_data with a category filter."""

    filters = Filters(category=[Some.CATEGORY])  # type: ignore[call-arg]
    filtered_data = filter_data(mock_data, filters)

    expected_data_len = 2
    assert len(filtered_data) == expected_data_len
    assert all(filtered_data["category"] == "Electronics")


def test_filter_data_product_ids(mock_data: pd.DataFrame) -> None:
    """Test filter_data with a product IDs filter."""

    filters = Filters(product_ids=[1001, 1004])  # type: ignore[call-arg]
    filtered_data = filter_data(mock_data, filters)

    expected_data_len = 2
    assert len(filtered_data) == expected_data_len
    assert set(filtered_data["product_id"]) == {1001, 1004}


def test_filter_data_no_matching_rows(mock_data: pd.DataFrame) -> None:
    """Test filter_data when no rows match the filters."""

    filters = Filters(
        date_range=Some.DATE_RANGE,
        category=["Home & Garden"],
        product_ids=[9999],
    )
    filtered_data = filter_data(mock_data, filters)

    expected_len_data = 0
    assert len(filtered_data) == expected_len_data
    assert filtered_data.empty


def test_filter_data_invalid_field(mock_data: pd.DataFrame) -> None:
    """Test filter_data with an empty filter returns original data."""

    filters = Filters()  # type: ignore[call-arg]
    filtered_data = filter_data(mock_data, filters)
    pd.testing.assert_frame_equal(filtered_data, mock_data)


def test_filter_data_empty_dataframe() -> None:
    """Test filter_data with an empty DataFrame."""

    empty_data = pd.DataFrame(
        columns=[
            "date",
            "product_id",
            "category",
            "quantity_sold",
            "price_per_unit",
        ]
    )
    filters = Filters(  # type: ignore[call-arg]
        category=["Electronics"],
    )
    filtered_data = filter_data(empty_data, filters)
    assert filtered_data.empty


def test_compute_statistics_valid(mock_data: pd.DataFrame) -> None:
    """Test compute_statistics with valid numerical columns."""
    columns = ["quantity_sold", "price_per_unit"]
    result = compute_statistics(mock_data, columns)

    quantity_mean = 25
    quantity_median = 25
    quantity_mode = 10
    quantity_percentile_25 = 17.5
    quantity_percentile_75 = 32.5

    price_mean = 20
    price_median = 20
    price_mode = 5
    price_percentile_25 = 12.5
    price_percentile_75 = 27.5

    # quantity_sold column
    assert "quantity_sold" in result
    assert result["quantity_sold"]["mean"] == quantity_mean
    assert result["quantity_sold"]["median"] == quantity_median
    assert result["quantity_sold"]["mode"] == quantity_mode
    assert result["quantity_sold"]["std_dev"] is not None
    assert result["quantity_sold"]["std_dev"] > 0
    assert result["quantity_sold"]["percentile_25"] == quantity_percentile_25
    assert result["quantity_sold"]["percentile_75"] == quantity_percentile_75

    # price_per_unit column
    assert "price_per_unit" in result
    assert result["price_per_unit"]["mean"] == price_mean
    assert result["price_per_unit"]["median"] == price_median
    assert result["price_per_unit"]["mode"] == price_mode
    assert result["price_per_unit"]["std_dev"] is not None
    assert result["price_per_unit"]["std_dev"] > 0
    assert result["price_per_unit"]["percentile_25"] == price_percentile_25
    assert result["price_per_unit"]["percentile_75"] == price_percentile_75


def test_compute_statistics_missing_columns(mock_data: pd.DataFrame) -> None:
    """Test compute_statistics when columns are missing in the DataFrame."""
    columns = ["non_existent_column", "quantity_sold"]
    result = compute_statistics(mock_data, columns)

    assert "quantity_sold" in result
    assert "non_existent_column" not in result


def test_compute_statistics_empty_dataframe() -> None:
    """Test compute_statistics with an empty DataFrame."""
    empty_data = pd.DataFrame(columns=["quantity_sold", "price_per_unit"])
    columns = ["quantity_sold", "price_per_unit"]
    result = compute_statistics(empty_data, columns)

    assert result == {}


def test_compute_statistics_nan_values() -> None:
    """Test compute_statistics with NaN values in the column."""
    data_with_nans = pd.DataFrame(
        {
            "quantity_sold": [10, 20, "Bilbo Baggins", None, 40],
        }
    )
    columns = ["quantity_sold"]

    # Define expected results as lowercase constants
    expected_mean = 23.333333333333332
    expected_median = 20
    expected_mode = 10
    expected_percentile_25 = 15
    expected_percentile_75 = 30

    result = compute_statistics(data_with_nans, columns)

    assert "quantity_sold" in result
    assert result["quantity_sold"]["mean"] == expected_mean
    assert result["quantity_sold"]["median"] == expected_median
    assert result["quantity_sold"]["mode"] == expected_mode
    assert result["quantity_sold"]["percentile_25"] == expected_percentile_25
    assert result["quantity_sold"]["percentile_75"] == expected_percentile_75
