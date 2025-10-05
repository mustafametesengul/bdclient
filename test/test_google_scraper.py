import asyncio

from bdclient.scraper.google.serp import CollectByURL, CollectByURLQuery
from bdclient.settings import Settings


async def main() -> None:
    keyword = "Latest News"

    settings = Settings()

    query = CollectByURLQuery(keyword=keyword)
    scraper = CollectByURL(api_key=settings.bright_data_api_key, limit_per_input=2)

    results = await scraper.scrape([query])

    for result in results:
        print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
