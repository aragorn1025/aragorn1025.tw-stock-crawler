"""Google Sheets API service."""

from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GSheetService:
    """Service for interacting with Google Sheets.

    Parameters:
        credentials_file (str):
            The path to the service account credentials JSON file.
    """

    def __init__(self, credentials_file: str) -> None:
        self.spreadsheets = build(
            "sheets",
            "v4",
            credentials=Credentials.from_service_account_file(
                credentials_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            ),
        ).spreadsheets()

    def read(self, spreadsheet_id: str, sheet_name: str, cells: str) -> list[list[Any]]:
        """Read data from the specified Google Sheet.

        Parameters:
            spreadsheet_id (str):
                The ID of the Google Spreadsheet to interact with.
            sheet_name (str):
                The name of the sheet within the spreadsheet to read from.
            cells (str):
                The cell range to read, e.g., "A1:C10".
        Returns:
            list[list[Any]]:
                A list of rows, where each row is a list of cell values.
        """
        result = self.spreadsheets.values().get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!{cells}").execute()
        # print(result)
        return result.get("values", [])

    def update(self, spreadsheet_id: str, sheet_name: str, cells: str, values: list[list[Any]]) -> dict:
        """Update the Google Sheet with new data.

        Parameters:
            spreadsheet_id (str):
                The ID of the Google Spreadsheet to interact with.
            sheet_name (str):
                The name of the sheet within the spreadsheet to update.
            cells (str):
                The cell range to update, e.g., "A1:C10".
            values (list[list[Any]]):
                A list of rows, where each row is a list of cell values to write.
        Returns:
            dict:
                The response from the Google Sheets API after the update operation.
        """
        return (
            self.spreadsheets.values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!{cells}",
                valueInputOption="RAW",
                body={"values": values},
            )
            .execute()
        )
