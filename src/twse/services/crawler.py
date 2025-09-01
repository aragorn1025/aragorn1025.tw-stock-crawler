"""TWSE Crawler Service."""

import requests

from ..errors import TWSEAPIError, TWSEDataError


class TWSECrawler:
    """Data crawler for TWSE stock price.

    Parameters:
        timeout (int):
            The timeout for the API request in seconds. Default is 5 seconds.
    """

    URL = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_AVG"
    HEADER = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}

    def __init__(
        self,
        timeout: int = 5,
    ) -> None:
        self.timeout = timeout

    def crawl(
        self,
        stock_number: str,
        year: int,
        month: int,
    ) -> list[list[str]]:
        """Crawl stock data for a specific stock number, year, and month.

        Parameters:
            stock_number (str):
                The stock number to crawl data for.
            year (int):
                The year of the data to crawl.
            month (int):
                The month of the data to crawl.
        Returns:
            list[list[str]]:
                A list of lists containing the stock data. Each inner list contains the date and stock price.
        Raises:
            TWSEAPIError:
                If the API request fails.
            TWSEDataError:
                If the data returned by the API is not valid.
        """
        response = requests.get(
            self.URL,
            params={
                "stockNo": stock_number,
                "date": f"{year}{month:02}01",
                "response": "json",
            },
            headers=self.HEADER,
            timeout=self.timeout,
            verify=False,
        )
        if response.status_code != 200:
            raise TWSEAPIError
        data = response.json()
        if data.get("stat") != "OK":
            raise TWSEDataError
        return data.get("data")[:-1]
