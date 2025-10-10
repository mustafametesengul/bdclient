from bdclient.unlocker import Unlocker

from .conftest import Settings


async def test_unlocker(settings: Settings) -> None:
    url = "https://www.bbc.com/news/articles/c8ex2l58en4o"
    zone = "web_unlocker1"

    unlocker = Unlocker(
        api_key=settings.bright_data_api_key,
        zone=zone,
    )

    result = await unlocker.unlock(url)
    print(result)
