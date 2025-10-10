from bdclient.scraper.google_serp import CollectByURL, CollectByURLQuery

from .conftest import Settings


async def test_google_serp(settings: Settings) -> None:
    keyword = "Latest News"

    query = CollectByURLQuery(keyword=keyword)
    scraper = CollectByURL(api_key=settings.bright_data_api_key, limit_per_input=2)

    results = await scraper.scrape([query])
    for result in results:
        print(result.model_dump_json(indent=4))
