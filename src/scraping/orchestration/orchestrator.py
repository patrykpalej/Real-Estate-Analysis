import re
import json
import fire
import logging
from dotenv import load_dotenv
from datetime import datetime

from utils.general import random_sleep
from utils.math import calc_perc
from utils.scraping import generate_scraper_name
from data.models.otodom import OtodomOffer
from data.storage.manager import StorageManager
from scraping.orchestration.reports import (ScrapingReport,
                                            SearchScrapingReport,
                                            OffersScrapingReport)
from scraping.logger import setup_logger
from scraping.otodom import OtodomSearchParams
from scraping.orchestration import (OtodomFiltersPath,
                                    DomiportaFiltersPath,
                                    OtodomSearchParamsSet,
                                    DomiportaSearchParamsSet,
                                    OtodomScrapers,
                                    DomiportaScrapers,
                                    JobTypes)
from scraping.orchestration.messaging import (SearchEmailSender,
                                              ScrapeEmailSender)
from exceptions import ServiceNotExists


class ScrapingOrchestrator:
    def __init__(self,
                 service_name: str,
                 property_type: str,
                 scraper_name: str = None,
                 job_type: str = None,
                 mode: int = 0):

        self.service_name = service_name
        self.mode = mode
        self.property_type = property_type
        self.scraper = self._get_scraper_class()(scraper_name)
        self.storage_manager = StorageManager(self.service_name,
                                              self.property_type,
                                              scraper_name,
                                              self.mode)
        if job_type == JobTypes.SEARCH.value:
            self.report = SearchScrapingReport()
        elif job_type == JobTypes.SCRAPE.value:
            self.report = OffersScrapingReport()
        else:
            self.report = ScrapingReport()
        self.report.scraping_started = datetime.now()

        self._log = logging.getLogger(scraper_name)
        self._log.info(f"Orchestrator initialized for {self.service_name} "
                       f"{self.property_type} | mode: {self.mode}")

    def _get_scraper_class(self) -> type:
        """
        Returns a proper scraper class
        """
        match self.service_name:
            case "OTODOM":
                return OtodomScrapers.__dict__[self.property_type].value
            case "DOMIPORTA":
                return DomiportaScrapers.__dict__[self.property_type].value
            case _ as value:
                raise ServiceNotExists(f"Service {value} does not exist")

    def _get_default_search_params(self) -> OtodomSearchParams:
        """
        Returns a proper class with default search params
        based on property type
        """
        match self.service_name:
            case "OTODOM":
                return OtodomSearchParamsSet.__dict__[self.property_type].value()
            case "DOMIPORTA":
                return DomiportaSearchParamsSet.__dict__[self.property_type].value()
            case _ as value:
                raise ServiceNotExists(f"Service {value} does not exist")

    def _get_custom_search_params(self) -> dict:
        """
        Returns a dict with custom search parameters based on service name
        and property
        """
        match self.service_name:
            case "OTODOM":
                path = OtodomFiltersPath.__dict__[self.property_type].value
            case "DOMIPORTA":
                path = DomiportaFiltersPath.__dict__[self.property_type].value
            case _ as value:
                raise ServiceNotExists(f"Service {value} does not exist")

        with open(path, "r") as file:
            custom_search_params = json.load(file)

        return custom_search_params

    def _combine_search_params(self, default_search_params: OtodomSearchParams,
                               custom_search_params: dict) -> (dict, int):
        """
        Combines default and custom search params (filters)

        Returns:
            (dict): dict of search params / filters
            (int): number of pages to search
        """
        self._log.debug("Search params combining started")

        search_params_dict = default_search_params.to_dict()
        search_params_dict.update(custom_search_params["filters"])

        self._log.debug("Search params combining ended")
        self._log.debug(f"All search params: {search_params_dict}. "
                        f"Number of pages: {custom_search_params['n_pages']}")

        return search_params_dict, custom_search_params["n_pages"]

    def search_offers_urls(self, cache: bool = True,
                           avg_sleep_time: int = 2) -> list[str]:
        """
        Searches for offers urls based on search params and saves urls to Redis
        """
        self._log.info("Searching offers urls started")

        default_search_params = self._get_default_search_params()
        custom_search_params = self._get_custom_search_params()

        all_search_params, n_pages_to_scrape = self._combine_search_params(
            default_search_params, custom_search_params)

        offers_urls, n_of_urls_from_pages = self.scraper.list_offers_urls_from_search_params(
            all_search_params, n_pages_to_scrape, avg_sleep_time)
        self.report.n_of_urls_acquired_from_pages = n_of_urls_from_pages

        if cache:
            self._log.debug("Caching offers urls started")
            cache_key_name = f"{self.scraper.name}_{len(offers_urls)}"
            self.storage_manager.cache_data(cache_key_name, offers_urls)
            self._log.debug("Caching offers urls ended")

        return offers_urls

    def scrape_cached_urls(self,
                           cache_pattern: str,
                           clear_cache: bool = True,
                           avg_sleep_time: int = 2):
        """
        Reads cached URLs based on a given pattern and scrapes them
        """
        self._log.info("Scraping cached offers started")

        all_keys = self.storage_manager.redis_db.scan_iter()
        matching_keys = [key
                         for key in all_keys
                         if re.match(cache_pattern, key.decode())]

        self._log.debug(f"Cached files read: {matching_keys}")

        all_offers_scraped = []
        n_of_offers_to_scrape = 0
        for key in matching_keys:
            urls_in_db = self.storage_manager.get_from_postgresql(
                ("url",)).values

            urls_package = self.storage_manager.read_cache(key, from_json=True)
            n_of_offers_to_scrape += len(urls_package)
            self._log.debug(f"Scraping offers from {key},"
                            f" {len(urls_package)} offers to scrape")

            n_urls_from_package_scraped = 0
            self.report.n_of_offers_in_packages_attempted.append(0)
            for url in urls_package[:(None if self.mode else 8)]:
                self.report.n_of_offers_in_packages_attempted[-1] += 1
                if url in urls_in_db:
                    self._log.warning(f"URL {url} already in database")
                    self.report.n_of_offers_scraped_before += 1
                    continue

                random_sleep(avg_sleep_time)

                try:
                    offer_data_model = self.scraper.scrape_offer_from_url(url)
                    all_offers_scraped.append(offer_data_model)
                    n_urls_from_package_scraped += 1
                    self._log.info(f"Offer successfully scraped from {url}")
                except Exception as e:
                    self.report.n_of_unknown_errors += 1
                    self._log.warning(f"Offer scraping failed ({url})")
                    self._log.warning(f"Error: {str(type(e))}: {str(e)}")

            self.report.n_of_offers_in_packages_success.append(
                n_urls_from_package_scraped)

            self._log.debug(f"For {key}: {n_urls_from_package_scraped} offers"
                            f" scraped out of {len(urls_package)} "
                            f"({calc_perc(n_urls_from_package_scraped, len(urls_package))}%)")

            if clear_cache:
                self.storage_manager.clear_cache(key)
                self._log.debug(f"{key}: cache cleared after scraping")

        self._log.info(f"Altogether {len(all_offers_scraped)} offers scraped"
                       f" out of {n_of_offers_to_scrape} "
                       f"({calc_perc(len(all_offers_scraped), n_of_offers_to_scrape)}%)")
        return all_offers_scraped

    def store_scraped_offers(self, offers: list[OtodomOffer],
                             postgresql: bool = False,
                             mongodb: bool = False,
                             bigquery: bool = False):
        """
        Dumps scraped offers to one or many of databases
        """
        self._log.info(f"Storing {len(offers)} offers started in: "
                       f"{'postgres' if postgresql else ''} "
                       f"{'mongo' if mongodb else ''} "
                       f"{'big query' if bigquery else ''}")

        if postgresql:
            try:
                n_success = self.storage_manager.store_in_postgresql(offers)
                self.report.n_postgresql_success = n_success
                self._log.info(f"{n_success} offers stored in postgresql")
            except Exception as e:
                self._log.error("Storing data in postgresql failed")
                self._log.exception(e)

        if mongodb:
            try:
                n_success = self.storage_manager.store_in_mongodb(offers)
                self.report.n_mongo_success = n_success
                self._log.info(f"{n_success} offers stored in mongodb")
            except Exception as e:
                self._log.error("Storing data in mongodb failed")
                self._log.exception(e)

        if bigquery:
            try:
                self.storage_manager.store_in_bigquery(offers)
            except Exception as e:
                self._log.error("Storing data in bigquery failed")
                self._log.exception(e)


class Pipeline:
    @staticmethod
    def search(service_name, property_type, mode):
        job_type = JobTypes.SEARCH.value
        scraper_name = generate_scraper_name(service_name, property_type,
                                             job_type)
        logger = setup_logger(scraper_name)
        orchestrator = ScrapingOrchestrator(service_name.upper(),
                                            property_type.upper(),
                                            scraper_name,
                                            job_type,
                                            mode)

        orchestrator.search_offers_urls()
        orchestrator.report.scraping_ended = datetime.now()

        sender = SearchEmailSender(service_name, property_type)
        sender.send_email(orchestrator.report)

        logger.info("Report sent via email")
        logger.info("Scraping finished properly")

    @staticmethod
    def scrape(service_name, property_type, mode):
        job_type = JobTypes.SCRAPE.value
        scraper_name = generate_scraper_name(service_name, property_type,
                                             job_type)
        logger = setup_logger(scraper_name)
        orchestrator = ScrapingOrchestrator(service_name.upper(),
                                            property_type.upper(),
                                            scraper_name,
                                            job_type,
                                            mode)
        pattern = r".*OTODOM_LOTS_SEARCH.*"
        offers = orchestrator.scrape_cached_urls(pattern,
                                                 clear_cache=False,
                                                 avg_sleep_time=5)
        orchestrator.report.scraping_ended = datetime.now()

        logger.info(f"{len(offers)} cached offers scraped")

        orchestrator.store_scraped_offers(offers,
                                          postgresql=True, mongodb=True)

        sender = ScrapeEmailSender(service_name, property_type)
        sender.send_email(orchestrator.report)

        logger.info("Report sent via email")
        logger.info("Scraping finished properly")


if __name__ == "__main__":
    load_dotenv()
    fire.Fire(Pipeline)

    # # TODO: CLI - args: the following:
    # service_name = "OTODOM"  # OTODOM, DOMIPORTA
    # property_type = "LOTS"  # LOTS, HOUSES, APARTMENTS
    # job_type = "SCRAPE"  # SEARCH, SCRAPE
    # mode = 0  # 0, 1, 2

    # scraper_name = generate_scraper_name(service_name, property_type, job_type)
    # logger = setup_logger(scraper_name)

    # orchestrator = ScrapingOrchestrator(service_name, property_type,
    #                                     scraper_name, job_type, mode)

    # if job_type == "SEARCH":
    #     orchestrator.search_offers_urls()
    #     orchestrator.report.scraping_ended = datetime.now()
    #
    #     sender = SearchEmailSender(service_name, property_type)
    #     sender.send_email(orchestrator.report)
    #
    #     logger.info("Report sent via email")

    # if job_type == "SCRAPE":
        # pattern = r".*OTODOM_LOTS_SEARCH.*"
        # offers = orchestrator.scrape_cached_urls(pattern,
        #                                          clear_cache=False,
        #                                          avg_sleep_time=5)
        # orchestrator.report.scraping_ended = datetime.now()
        #
        # logger.info(f"{len(offers)} cached offers scraped")
        #
        # orchestrator.store_scraped_offers(offers,
        #                                   postgresql=True, mongodb=True)
        #
        # sender = ScrapeEmailSender(service_name, property_type)
        # sender.send_email(orchestrator.report)
        #
        # logger.info("Report sent via email")

    
