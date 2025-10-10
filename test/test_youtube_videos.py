from bdclient.scraper.youtube_videos import DiscoverByKeyword, DiscoverByKeywordQuery

from .conftest import Settings


async def test_youtube_videos(settings: Settings) -> None:
    keyword = "Latest News"

    query = DiscoverByKeywordQuery(keyword=keyword)
    scraper = DiscoverByKeyword(api_key=settings.bright_data_api_key, limit_per_input=2)

    results = await scraper.scrape([query])
    for result in results:
        print(result.model_dump_json(indent=4))
