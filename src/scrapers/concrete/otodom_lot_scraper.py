from scrapers.abstract.otodom_scraper import OtodomScraper


class OtodomLotScraper(OtodomScraper):
    SUB_URL: str = "pl/oferty/sprzedaz/dzialka/cala-polska"

    def __init__(self, scraper_name):
        super().__init__(scraper_name)

    def parse_soup(self):
        pass


if __name__ == "__main__":
    ols = OtodomLotScraper("test")

    search_dict = {"ownerTypeSingleSelect": "ALL",
                   "viewType": "listing",
                   "limit": "72",
                   "page": "1"}

    urls_list = ols.list_offers_urls_from_search(search_dict)
    print(urls_list)
