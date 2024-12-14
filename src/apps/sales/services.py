"""File containing business logic for sales app."""

import pandas as pd

from src.apps.sales.const import EXPECTED_COLUMNS
from src.core.settings import settings


def load_data() -> pd.DataFrame:
    """Load sales data from CSV file."""

    try:
        data = pd.read_csv(settings.sales_data)

    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Sales data file not found at {settings.sales_data}"
        ) from err

    except pd.errors.EmptyDataError as err:
        message = "Sales data file is empty"
        raise ValueError(message) from err

    _validate_correct_columns(data)
    return data


def _validate_correct_columns(data: pd.DataFrame) -> None:
    """Validate that the sales DataFrame contains the required columns."""

    expected_columns = EXPECTED_COLUMNS
    if not expected_columns.issubset(data.columns):
        error_data = "Sales data file does not contain the required columns"
        raise ValueError(error_data)
