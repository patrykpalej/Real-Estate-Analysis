# Real Estate Analysis
Data scraper and analytical solutions for real estate market analysis

## Data gathering
There are two services used as data sources in the project:
- Otodom
- Domiporta

For each service the following property types are scraped:
- Lots
- Houses
- Apartments

## CLI
There is a CLI which can be used to interact with the scrapers.

...

## Tests
To run tests in terminal `cd` to `tests/` directory and run:

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
