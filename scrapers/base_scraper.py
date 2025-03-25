from typing import List
from bs4 import BeautifulSoup
import requests
import time
import logging
from abc import ABC, abstractmethod

from scrapers.models.coffee_varietal import CoffeeVarietal


class BaseScraper(ABC):

    HEADERS = {}

    def __init__(self, base_url: str, max_retries: int = 3, delay: float = 1.0):
        self.base_url = base_url
        self.max_retries = max_retries
        self.delay = delay

    def fetch_url(self) -> BeautifulSoup:
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(
                    self.base_url, headers=self.HEADERS, timeout=10)
                response.raise_for_status()
                raw_data = BeautifulSoup(response.text, "html.parser")
                return raw_data
            except requests.RequestException as e:
                logging.warning(
                    f"Request failed: {e}, retrying ({retries+1}/{self.max_retries})")
                retries += 1
                time.sleep(self.delay)
        raise requests.RequestException(
            f"Failed to fetch {self.base_url} after {self.max_retries} retries.")

    def store_data(self, data: List[CoffeeVarietal]):
        for item in data:
            print(item)
        pass

    @abstractmethod
    def parse_data(self, raw_data: BeautifulSoup) -> List[CoffeeVarietal]:
        pass

    def run(self):
        raw_data = self.fetch_url()
        if raw_data:
            varietal_data: List[CoffeeVarietal]
            varietal_data = self.parse_data(raw_data)
            self.store_data(varietal_data)
        return None
