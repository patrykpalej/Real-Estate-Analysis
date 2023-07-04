import json
from abc import ABC, abstractmethod
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from utils.general import random_sleep
from scraping.abstract.property_scraper import PropertyScraper
from scraping import Services
from data.models.otodom import OtodomOffer
from scraping.orchestration.reports import (SearchScrapingReport,
                                            OffersScrapingReport)


class OtodomScraper(PropertyScraper, ABC):
    SERVICE_NAME: str = Services.OTODOM.value
    BASE_URL: str = "https://www.otodom.pl/"
    OFFER_BASE_URL: str = "https://www.otodom.pl/pl/oferta/"
    SUB_URL: None

    def __init__(self, scraper_name: str):
        super().__init__(scraper_name)

    @abstractmethod
    def _parse_offer_soup(self, offer_soup: BeautifulSoup):
        raise NotImplementedError

    @staticmethod
    def _get_raw_offer_data_from_offer_soup(offer_soup: BeautifulSoup) -> dict:
        """
        Takes a soup of a single offer page and returns raw offer data (JSON)
        """
        offer_data = offer_soup.find("script", {"id": "__NEXT_DATA__"}).text
        offer_full_json = json.loads(offer_data)
        offer_json = offer_full_json["props"]["pageProps"]["ad"]
        return offer_json

    def _get_offers_urls_from_single_search_page(
            self, search_page_soup: BeautifulSoup) -> list[str]:
        """
        Scrapes a single page of search results and returns offers urls

        Args:
            search_page_soup (BeautifulSoup): bs4 soup of a single search page

        Returns:
            (list[str]): list of urls found on the search page
        """
        all_scripts = search_page_soup.find_all("script",
                                                {"type": "application/json"})

        try:
            offers_script_idx = 0
            offers_json = json.loads(all_scripts[offers_script_idx].text)
        except IndexError:
            self._log.warning("Offers script not found on the search page")
            return []

        try:
            offers_list = (offers_json["props"]["pageProps"]["data"]
                                      ["searchAds"]["items"])
        except KeyError:
            self._log.warning("Offers search JSON invalid (keys not found)")
            return []

        offers_slugs = [offer["slug"] for offer in offers_list]
        offers_urls = [self.OFFER_BASE_URL + slug for slug in offers_slugs]

        return offers_urls

    def scrape_offer_from_url(self, url: str) -> OtodomOffer:
        """
        Takes a URL to an offer and returns a data model for that offer
        """
        response = self._request_http_get(url,
                                          headers=self._generate_headers())
        offer_soup = self._make_soup(response)
        offer_data_model = self._parse_offer_soup(offer_soup)
        return offer_data_model

    def list_offers_urls_from_search_params(
            self, search_params: dict, n_pages: int,
            avg_sleep_time: int = 2) -> (list[str], list[int]):
        """
        Based on complete dict of search filters (default and custom)
        and `n_pages` to scrape returns a list of urls from all those pages.

        Args:
            search_params (dict): default and custom filters
            n_pages (int): number of pages to search
            avg_sleep_time (int): avg. n. of secs. to sleep between requests

        Returns:
            (list[str]): list of urls to offers from all N pages
            (list[int]): number of urls aquired from subsequent pages
        """
        all_urls_list = []
        n_of_urls_from_pages = []
        self._log.debug(f"About to scrape {n_pages} pages")
        for page_number in range(n_pages):
            page_number += 1
            random_sleep(avg_sleep_time)
            random_headers = self._generate_headers()
            search_url = urljoin(self.BASE_URL, self.SUB_URL)
            search_params.update({"page": page_number})

            search_response = self._request_http_get(search_url,
                                                     headers=random_headers,
                                                     params=search_params)

            self._log.debug(f"Requested search url: {search_response.url} ")

            search_soup = self._make_soup(search_response)
            try:
                page_urls_list = self._get_offers_urls_from_single_search_page(
                    search_soup)
                n_of_urls_from_pages.append(len(page_urls_list))
            except Exception as e:
                self._log.exception(e)
                page_urls_list = []

            self._log.debug(f"Got {len(page_urls_list)} urls from search page")

            all_urls_list.extend(page_urls_list)

            if not page_urls_list:
                self._log.warning("No urls found on a search page. "
                                  "Searching aborted")
                break

        self._log.info(f"Found {len(all_urls_list)} urls from search params")
        return all_urls_list, n_of_urls_from_pages
