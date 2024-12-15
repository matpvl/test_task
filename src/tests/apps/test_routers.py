"""Tests for WebServices."""

from http.client import OK
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Assume your main application file is named `main.py` and defines `app`
from main import app
from src.apps.sales.dto import SummaryRequest, Filters
from src.core.settings import settings
from src.tests.const import Some


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Fixture to provide a test client and mock data file for the summary endpoint."""

    # Create a temporary CSV file with mock data
    csv_content = """date,product_id,category,quantity_sold,price_per_unit
2023-01-01,1001,Electronics,10,5.0
2023-01-15,1002,Clothing,20,15.0
2023-01-20,1003,Electronics,30,25.0
2023-02-01,1004,Clothing,40,35.0
    """
    file_path = tmp_path / "sales_data.csv"
    file_path.write_text(csv_content)

    # Monkeypatch the settings to point to our temporary CSV
    monkeypatch.setattr(settings, "sales_data", file_path)

    return TestClient(app)


def test_generate_sales_summary_no_filters(client: TestClient) -> None:
    """Test the /summary endpoint with default columns and no filters."""

    payload = SummaryRequest().model_dump()
    response = client.post("/summary", json=payload)

    assert response.status_code == OK

    response_data = response.json()
    # We expect both columns to be present since default columns are used.
    assert "summary" in response_data
    assert "quantity_sold" in response_data["summary"]
    assert "price_per_unit" in response_data["summary"]

    expected_quantity_mean = 25
    expected_quantity_median = 25
    expected_quantity_mode = 10
    expected_quantity_percentile_25 = 17.5
    expected_quantity_percentile_75 = 32.5

    expected_price_mean = 20
    expected_price_median = 20
    expected_price_mode = 5
    expected_price_percentile_25 = 12.5
    expected_price_percentile_75 = 27.5

    # Check that statistics have been computed correctly
    quantity_stats = response_data["summary"]["quantity_sold"]
    assert quantity_stats["mean"] == expected_quantity_mean
    assert quantity_stats["median"] == expected_quantity_median
    assert quantity_stats["mode"] == expected_quantity_mode
    assert quantity_stats["percentile_25"] == expected_quantity_percentile_25
    assert quantity_stats["percentile_75"] == expected_quantity_percentile_75

    price_stats = response_data["summary"]["price_per_unit"]
    assert price_stats["mean"] == expected_price_mean
    assert price_stats["median"] == expected_price_median
    assert price_stats["mode"] == expected_price_mode
    assert price_stats["percentile_25"] == expected_price_percentile_25
    assert price_stats["percentile_75"] == expected_price_percentile_75


def test_generate_sales_summary_with_date_filter(client: TestClient) -> None:
    """Test date filter works accordingly."""

    filters = Filters(date_range=Some.DATE_RANGE)
    payload = SummaryRequest(filters=filters).model_dump(mode="json")
    response = client.post("/summary", json=payload)

    assert response.status_code == OK
    response_data = response.json()

    expected_quantity_mean = 20
    expected_price_mean = 15

    assert "summary" in response_data
    assert "quantity_sold" in response_data["summary"]
    assert "price_per_unit" in response_data["summary"]

    quantity_stats = response_data["summary"]["quantity_sold"]
    assert quantity_stats["mean"] == expected_quantity_mean

    price_stats = response_data["summary"]["price_per_unit"]
    assert price_stats["mean"] == expected_price_mean


def test_generate_sales_summary_with_category_filter(
    client: TestClient,
) -> None:
    """Test filtering via electronics row."""

    filters = Filters(category=["Electronics"])
    payload = SummaryRequest(filters=filters).model_dump()
    response = client.post("/summary", json=payload)

    assert response.status_code == OK
    response_data = response.json()

    expected_quantity_median = 20
    expected_price_median = 15

    quantity_stats = response_data["summary"]["quantity_sold"]
    assert quantity_stats["median"] == expected_quantity_median

    price_stats = response_data["summary"]["price_per_unit"]
    assert price_stats["median"] == expected_price_median


def test_generate_sales_summary_no_matching_filters(client: TestClient) -> None:
    """Test the /summary endpoint when filters match no rows."""

    filters = Filters(category=["NonExistentCategory"])
    payload = SummaryRequest(filters=filters).model_dump()
    response = client.post("/summary", json=payload)

    assert response.status_code == OK
    response_data = response.json()

    # no matching rows, so no statistics
    assert response_data == {"summary": {}}


def test_generate_sales_summary_custom_columns(client: TestClient) -> None:
    """Test the summary endpoint requesting only one column: quantity_sold."""

    payload = SummaryRequest(columns=["quantity_sold"]).model_dump()
    response = client.post("/summary", json=payload)

    assert response.status_code == OK
    response_data = response.json()

    # Only "quantity_sold" should be present
    assert "quantity_sold" in response_data["summary"]
    assert "price_per_unit" not in response_data["summary"]

    expected_number_of_statistics_fields = 6
    assert (
        len(response_data["summary"]["quantity_sold"])
        == expected_number_of_statistics_fields
    )