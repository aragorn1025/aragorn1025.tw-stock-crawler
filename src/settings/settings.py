"""Settings class for TWSE stock data crawler."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the TWSE stock data crawler."""

    is_output_csv: bool = False
    csv_path: str = ""

    is_output_gsheet: bool = False
    gsheet_service_account_credentials: str = ""
    gsheet_spreadsheet_id: str = ""
    gsheet_sheet_name: str = ""
    gsheet_top_left_cell: str = ""


settings = Settings()
