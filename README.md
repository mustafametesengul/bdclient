# BDClient

An unofficial Python client for Bright Data APIs.

## Installation

Installing using pip:
```
pip install bdclient
```

## Usage

Example usage:
```python
import asyncio

from bdclient.scraper.youtube.videos import DiscoverByKeyword, DiscoverByKeywordQuery


async def main():
    scraper = DiscoverByKeyword(api_key="your_api_key")
    query = DiscoverByKeywordQuery(keyword="Latest News")

    results = await scraper.scrape([query])
    for result in results:
        print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
```
