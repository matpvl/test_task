"""File containing business logic for sales app."""

import pandas as pd

from src.core.settings import settings


def load_data() -> pd.DataFrame:
    """Load sales data from CSV file."""

    try:
        return pd.read_csv(settings.sales_data)

    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Sales data file not found at {settings.sales_data}"
        ) from err

    except pd.errors.EmptyDataError as err:
        message = "Sales data file is empty"
        raise ValueError(message) from err

    except pd.errors.ParserError as err:
        message = f"Error parsing sales data file: {err}"
        raise ValueError(message) from err
