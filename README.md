# Real Estate Market Analysis
Data scraper and analytical solutions for real estate market analysis

## Used technologies

**Web scraping**
- Python (requests, bs4)

**Data storage**
- PostgreSQL
- MongoDB
- Redis

**Data visualization**
- Streamlit


## Data gathering
There are two services used as data sources in the project:
- Otodom
- Domiporta

For each service, the following property types are scraped:
- Lands
- Houses
- Apartments

### CLI
There is a CLI which can be used to interact with the scrapers.

The CLI can be accessed by running `src/scraping/orchestration/orchestrator.py` module with one of the following values as a first argument:
- `search` (searches for urls and dumps them to redis) 
- `scrape` (loads urls from redis, scrapes them and dumps to postgresql and mongo)

The next argument arguments are:

`service_name`, which accepts the following values:
- `otodom`
- `domiporta`

`property_typ`, which accepts:
- `houses`
- `lands`
- `apartments`

`mode`:
- 0 (test)
- 1 (dev)
- 2 (prod)

Each mode operates on a different database instance.

Running the scraper via CLI can be easily automated e.g. using crontab.


## Tests
To run tests in terminal, `cd` to `tests/`, set `PYTHONPATH` to `src/` directory and run:

`python -m unittest discover`

---

To check % of coverage run:
```
coverage run -m unittest discover -p "test_*.py"
python -m coverage report [--skip-empty] [--show-missing] [--skip-covered]
```
e.g.
```
coverage run -m unittest discover -p "test_*.py"
python -m coverage report --skip-empty --show-missing --skip-covered
```

## Dashboard

There is a Streamlit analytical dashboard included which allows to visualize distribution of data.

More features to be added in the future.






