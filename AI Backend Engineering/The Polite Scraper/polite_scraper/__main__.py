from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from .crawler import CrawlConfig, PoliteCrawler

START_URL = "https://books.toscrape.com/"


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Crawl a bounded portion of Books to Scrape politely.")
    parser.add_argument("--max-pages", type=int, default=2)
    parser.add_argument("--output-dir", default=os.getenv("SCRAPER_OUTPUT_DIR", "data"))
    args = parser.parse_args()
    config = CrawlConfig(
        start_url=START_URL,
        user_agent=os.getenv("SCRAPER_USER_AGENT", "HabibPoliteScraper/1.0 (+https://github.com/iam-habib-rehman12/FlyRank)"),
        delay_seconds=float(os.getenv("SCRAPER_DELAY_SECONDS", "1.5")),
        timeout_seconds=float(os.getenv("SCRAPER_TIMEOUT_SECONDS", "15")),
        max_retries=int(os.getenv("SCRAPER_MAX_RETRIES", "3")),
        max_pages=args.max_pages,
    )
    records = [record.as_dict() for record in PoliteCrawler(config).crawl()]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "books.jsonl"
    csv_path = output_dir / "books.csv"
    with jsonl_path.open("w", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]) if records else [])
        if records:
            writer.writeheader()
            writer.writerows(records)
    print(f"Saved {len(records)} records to {jsonl_path} and {csv_path}")


if __name__ == "__main__":
    main()

