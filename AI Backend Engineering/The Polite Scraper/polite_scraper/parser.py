from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
import re
import unicodedata
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def clean_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    return re.sub(r"\s+", " ", value).strip()


@dataclass(frozen=True)
class BookRecord:
    source_url: str
    title: str
    category: str
    description: str
    price_gbp: str
    availability: str
    rating: int
    upc: str
    scraped_at: str

    def as_dict(self) -> dict[str, str | int]:
        return asdict(self)


def _same_origin(base_url: str, candidate: str) -> bool:
    return urlparse(base_url).netloc == urlparse(candidate).netloc


def parse_catalogue(html: str, page_url: str) -> tuple[list[str], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    product_urls: list[str] = []
    for anchor in soup.select("article.product_pod h3 a[href]"):
        url = urljoin(page_url, anchor["href"])
        if _same_origin(page_url, url):
            product_urls.append(url)
    next_link = soup.select_one("li.next a[href]")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    if next_url and not _same_origin(page_url, next_url):
        next_url = None
    return list(dict.fromkeys(product_urls)), next_url


def parse_book(html: str, source_url: str, scraped_at: str) -> BookRecord:
    soup = BeautifulSoup(html, "html.parser")
    title = clean_text(soup.select_one("div.product_main h1").get_text())
    price_text = clean_text(soup.select_one("p.price_color").get_text()).replace("Â£", "")
    price = format(Decimal(price_text), ".2f")
    availability = clean_text(soup.select_one("p.instock.availability").get_text())
    rating_node = soup.select_one("p.star-rating")
    rating = next((RATINGS[name] for name in RATINGS if name in rating_node.get("class", [])), 0)
    crumbs = [clean_text(a.get_text()) for a in soup.select("ul.breadcrumb li a")]
    category = crumbs[-1] if crumbs else ""
    description_heading = soup.find(id="product_description")
    description_node = description_heading.find_next_sibling("p") if description_heading else None
    description = clean_text(description_node.get_text()) if description_node else ""
    details = {
        clean_text(row.th.get_text()): clean_text(row.td.get_text())
        for row in soup.select("table.table.table-striped tr")
    }
    return BookRecord(source_url, title, category, description, price, availability, rating, details.get("UPC", ""), scraped_at)

