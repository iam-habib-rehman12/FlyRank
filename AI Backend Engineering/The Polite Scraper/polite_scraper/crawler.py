from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

from .parser import BookRecord, parse_book, parse_catalogue

TRANSIENT = {429, 500, 502, 503, 504}


@dataclass(frozen=True)
class CrawlConfig:
    start_url: str
    user_agent: str
    delay_seconds: float = 1.5
    timeout_seconds: float = 15
    max_retries: int = 3
    max_pages: int = 2


class PoliteCrawler:
    def __init__(self, config: CrawlConfig, session: requests.Session | None = None):
        if config.delay_seconds < 1:
            raise ValueError("delay_seconds must be at least 1")
        if config.max_pages < 1:
            raise ValueError("max_pages must be positive")
        self.config = config
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": config.user_agent})
        self.origin = urlparse(config.start_url).netloc
        self._last_request = 0.0
        self.robots = self._load_robots()

    def _wait(self) -> None:
        remaining = self.config.delay_seconds - (time.monotonic() - self._last_request)
        if remaining > 0:
            time.sleep(remaining)

    def _raw_get(self, url: str) -> requests.Response:
        for attempt in range(self.config.max_retries):
            self._wait()
            response = self.session.get(url, timeout=self.config.timeout_seconds)
            self._last_request = time.monotonic()
            if response.status_code not in TRANSIENT:
                response.raise_for_status()
                return response
            if attempt + 1 < self.config.max_retries:
                time.sleep(self.config.delay_seconds * (2**attempt))
        response.raise_for_status()
        raise RuntimeError("unreachable")

    def _load_robots(self) -> RobotFileParser:
        parsed = urlparse(self.config.start_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        parser = RobotFileParser(robots_url)
        self._wait()
        response = self.session.get(robots_url, timeout=self.config.timeout_seconds)
        self._last_request = time.monotonic()
        if response.status_code == 404:
            parser.parse([])
            return parser
        response.raise_for_status()  # fail closed when policy cannot be read
        parser.parse(response.text.splitlines())
        return parser

    def get(self, url: str) -> str:
        if urlparse(url).netloc != self.origin:
            raise ValueError(f"refusing off-origin URL: {url}")
        if not self.robots.can_fetch(self.config.user_agent, url):
            raise PermissionError(f"robots.txt disallows: {url}")
        return self._raw_get(url).text

    def crawl(self) -> list[BookRecord]:
        records: list[BookRecord] = []
        seen_products: set[str] = set()
        page_url: str | None = self.config.start_url
        pages = 0
        while page_url and pages < self.config.max_pages:
            product_urls, page_url = parse_catalogue(self.get(page_url), page_url)
            pages += 1
            for url in product_urls:
                if url in seen_products:
                    continue
                seen_products.add(url)
                now = datetime.now(timezone.utc).isoformat()
                records.append(parse_book(self.get(url), url, now))
        return records

