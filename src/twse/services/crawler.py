import requests

from ..errors import TWSEAPIError, TWSEDataError


class TWSECrawler:
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
