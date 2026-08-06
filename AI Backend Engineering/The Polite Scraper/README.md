# The Polite Scraper

A small, production-minded Python crawler for [Books to Scrape](https://books.toscrape.com/), a sandbox that explicitly welcomes scraping. It follows the complete data pipeline:

`fetch -> parse -> extract -> clean -> structure -> save`

## Politeness contract

- Reads and honors `robots.txt` before crawling. A missing `robots.txt` (HTTP 404) means no published restrictions; any other retrieval failure stops the crawl.
- Sends an identifying `User-Agent` with a project URL.
- Waits at least 1.5 seconds between requests, including retries.
- Uses exponential backoff for `429`, `500`, `502`, `503`, and `504` only.
- Crawls only `books.toscrape.com`, deduplicates URLs, and has an explicit page limit.
- Never bypasses authentication, CAPTCHAs, or access controls.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows; use `cp` on macOS/Linux
python -m polite_scraper --max-pages 2
```

Outputs are written to `data/books.jsonl` and `data/books.csv`. Use `--help` for all options.

## Configuration

| Variable | Default | Purpose |
|---|---:|---|
| `SCRAPER_USER_AGENT` | project identifier | Identifies the crawler and links to its owner |
| `SCRAPER_DELAY_SECONDS` | `1.5` | Minimum delay between requests |
| `SCRAPER_TIMEOUT_SECONDS` | `15` | Per-request timeout |
| `SCRAPER_MAX_RETRIES` | `3` | Attempts for transient failures |
| `SCRAPER_OUTPUT_DIR` | `data` | Output directory |

CLI flags override environment values where applicable.

## Record schema

Each JSONL line is an independent RAG-ready source document with `source_url`, `title`, `category`, `description`, `price_gbp`, `availability`, `rating`, `upc`, and `scraped_at`. Text is Unicode-normalized and whitespace-collapsed; prices are stored as decimal strings to avoid floating-point errors. CSV contains the same fields for inspection.

## Verify

```bash
python -m unittest discover -s tests -v
python -m compileall polite_scraper tests
```

The tests use local HTML fixtures and never contact the live site. They prove extraction, cleaning, pagination discovery, same-origin filtering, and the missing-robots policy.

## Responsible use

This project is intentionally configured for a practice website. Before adapting it to another site, obtain permission when appropriate, review its terms and robots policy, lower the request rate if requested, and minimize collected personal data.

