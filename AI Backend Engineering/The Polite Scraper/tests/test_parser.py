import unittest

from polite_scraper.parser import clean_text, parse_book, parse_catalogue

CATALOGUE = '''<article class="product_pod"><h3><a href="catalogue/a/index.html">A</a></h3></article><li class="next"><a href="catalogue/page-2.html">next</a></li>'''
BOOK = '''
<ul class="breadcrumb"><li><a>Home</a></li><li><a>Books</a></li><li><a>Travel</a></li></ul>
<div class="product_main"><h1>  A   Book </h1><p class="price_color">Â£12.30</p><p class="instock availability"> In stock (3 available) </p><p class="star-rating Four"></p></div>
<div id="product_description"></div><p>A\n useful   description.</p>
<table class="table table-striped"><tr><th>UPC</th><td>abc-123</td></tr></table>'''


class ParserTests(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(clean_text(" A\n  B "), "A B")

    def test_catalogue_links_are_absolute(self):
        products, next_url = parse_catalogue(CATALOGUE, "https://books.toscrape.com/")
        self.assertEqual(products, ["https://books.toscrape.com/catalogue/a/index.html"])
        self.assertEqual(next_url, "https://books.toscrape.com/catalogue/page-2.html")

    def test_off_origin_links_are_rejected(self):
        products, _ = parse_catalogue(CATALOGUE.replace("catalogue/a/index.html", "https://evil.test/a"), "https://books.toscrape.com/")
        self.assertEqual(products, [])

    def test_book_is_clean_and_structured(self):
        record = parse_book(BOOK, "https://books.toscrape.com/a", "2026-08-06T00:00:00+00:00")
        self.assertEqual(record.title, "A Book")
        self.assertEqual(record.category, "Travel")
        self.assertEqual(record.description, "A useful description.")
        self.assertEqual(record.price_gbp, "12.30")
        self.assertEqual(record.rating, 4)
        self.assertEqual(record.upc, "abc-123")


if __name__ == "__main__":
    unittest.main()

