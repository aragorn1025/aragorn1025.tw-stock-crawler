"""Crawl stock data from TWSE and save as a CSV file."""

import argparse
import collections
import logging
import time

import pandas as pd
import urllib3

from twse.services import TWSECrawler
from utils import convert_roc_date, get_months

logging.basicConfig(
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    format="[%(asctime)s][%(levelname).1s] %(message)s",
    level=logging.INFO,
)


def crawl_all_data(
    stock_numbers: list[str],
    year: int,
    months: list[int] = None,
    sleep_time: int = 3,
) -> dict[str, list[list[str]]]:
    """Crawl stock data for multiple stock numbers and a specific year.

    Parameters:
        stock_numbers (list[str]):
            The list of stock numbers to crawl data for.
        year (int):
            The year in AD to crawl data for.
        months (list[int], optional):
            The list of months to crawl data for. If None, all available months of the year will be used.
        sleep_time (int, optional):
            The sleep time between requests in seconds. Default is 3 seconds.
    Returns:
        dict[str, list[list[str]]]:
            A dictionary where keys are stock numbers and values are lists of the stock data.
    Raises:
        ValueError:
            If the year is in the future.
        TWSEAPIError:
            If the API request fails.
        TWSEDataError:
            If the data returned by the API is not valid.
    """
    if not months:
        months = get_months(year)
    logging.info("Crawling data for %s in %s/%s", stock_numbers, year, months)
    crawler = TWSECrawler()
    all_data = collections.defaultdict(list)
    for stock_number in stock_numbers:
        data = all_data[stock_number]
        for month in months:
            data.extend(crawler.crawl(stock_number, year, month))
            time.sleep(sleep_time)
    return all_data


def convert_to_data_frame(all_data: dict[str, list[list[str]]]) -> pd.DataFrame:
    """Convert crawled stock data to a pandas DataFrame.
    Parameters:
        all_data (dict[str, list[list[str]]]):
            A dictionary where keys are stock numbers and values are lists of the stock data.
    Returns:
        pandas.DataFrame:
            A DataFrame with dates as the index and stock prices as columns.
    """
    dfs = []
    for stock_number, data in all_data.items():
        df = pd.DataFrame(data, columns=["date", stock_number])
        df["date"] = df["date"].apply(convert_roc_date)
        df = df.set_index("date")
        dfs.append(df)
    result_df = pd.concat(dfs, axis=1)

    full_date_range = pd.date_range(
        start=result_df.index.min().replace(day=1),
        end=result_df.index.max().replace(day=1) + pd.offsets.MonthEnd(0),
        freq="D",
    ).date
    result_df = result_df.reindex(full_date_range).fillna("")
    result_df.index.name = "date"
    return result_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl stock data and save as a CSV file.")
    parser.add_argument(
        "-s",
        "--stock_numbers",
        type=str,
        required=True,
        help="Stock numbers, separated by commas (e.g., 0050,006208)",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        required=True,
        help="Year in AD (e.g., 2025)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.csv",
        help="Output CSV file name (default: output.csv)",
    )
    args = parser.parse_args()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    all_stock_data = crawl_all_data(
        stock_numbers=args.stock_numbers.split(","),
        year=args.year,
    )
    result = convert_to_data_frame(all_stock_data)
    result.to_csv(args.output, encoding="utf-8")
