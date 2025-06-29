import argparse
import collections
import time

import pandas as pd
import urllib3

from twse.services import TWSECrawler
from utils import convert_roc_date, get_months


def crawl_all_data(
    stock_numbers: list[str],
    year: int,
    months: list[int] = None,
    sleep_time: int = 3,
) -> dict[str, list[list[str]]]:
    if not months:
        months = get_months(year)
    crawler = TWSECrawler()
    all_data = collections.defaultdict(list)
    for stock_number in stock_numbers:
        data = all_data[stock_number]
        for month in months:
            data.extend(crawler.crawl(stock_number, year, month))
            time.sleep(sleep_time)
    return all_data


def convert_to_data_frame(all_data: dict[str, list[list[str]]]) -> pd.DataFrame:
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
        nargs="+",
        required=True,
        help="Stock numbers, separated by space (e.g., 0050 006208)",
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
    all_stock_data = crawl_all_data(stock_numbers=args.stock_numbers, year=args.year)
    result = convert_to_data_frame(all_stock_data)
    result.to_csv(args.output, encoding="utf-8")
