"""Tests for the sales app business logic."""

import pytest
import pandas as pd

from pathlib import Path

from src.apps.sales.services import load_data
from src.core.settings import settings


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
