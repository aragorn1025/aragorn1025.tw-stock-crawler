"""Settings class for TWSE stock data crawler."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the TWSE stock data crawler."""

    is_output_csv: bool = False
    csv_path: str = ""


settings = Settings()
