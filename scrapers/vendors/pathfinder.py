import os
from typing import List
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv

from scrapers.base_scraper import BaseScraper
from scrapers.models.coffee_varietal import CoffeeVarietal

VALID_CATEGORIES = {"House coffee", "Decaffeinated",
                    "Special Espresso", "Special Filter", "Competition", "Fruity"}


class PathfinderScraper(BaseScraper):

    def __init__(self):
        load_dotenv()
        super().__init__(os.getenv("PATHFINDER_SITE_URL") or "")

    def parse_data(self, raw_data: BeautifulSoup) -> List[CoffeeVarietal]:
        varietal_data: List[CoffeeVarietal] = []
        for product in raw_data.find_all("div", class_="productItem"):
            if not isinstance(product, Tag):
                continue

            category_tag = product.find("h3", class_="pr-5 mb-5")
            if category_tag is None:
                raise ValueError("Category tag not found.")
            category = category_tag.text.strip()
            if category not in VALID_CATEGORIES:
                continue

            data_list_tag = product.select("div.w-4\/12.flex.flex-col span h3")
            if len(data_list_tag) != 3:
                raise ValueError("Data list tags not found.")
            roasting_profile = data_list_tag[0].text.strip()
            origin = data_list_tag[1].text.strip()
            producer = data_list_tag[2].text.strip()
            name = f'{roasting_profile}-{origin}-{producer}'

            notes_tag = product.select_one(
                "div.w-4\/12.lg\\:px-\\[11px\\] span")
            if notes_tag is None:
                raise ValueError("Notes tag not found.")
            notes = [note.strip()
                     for note in notes_tag.get_text(separator="|").split("|")]

            price_tag = product.select_one("span[data-product-price]")
            if price_tag is None:
                raise ValueError("Price tag not found.")
            price = float(price_tag.get_text(separator="|").split(
                "|")[1].replace("€", "").replace(",", "."))

            varietal_data.append(CoffeeVarietal(
                name=name,
                origin=origin,
                producer=producer,
                roasting_profile=roasting_profile,
                price=price,
                notes=notes,
                category=category
            ))

        return varietal_data