"""Sales application constants."""
from pathlib import Path

ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()
SALES_DATA: Path = ROOT_DIR / "sales_data.csv"
