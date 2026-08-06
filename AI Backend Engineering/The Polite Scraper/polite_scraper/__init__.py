"""A bounded, robots-aware scraper for a practice catalogue."""

from .parser import BookRecord, parse_book, parse_catalogue

__all__ = ["BookRecord", "parse_book", "parse_catalogue"]

