import asyncio

from bdclient.settings import Settings
from bdclient.unlocker import Unlocker


async def main() -> None:
    url = "https://www.bbc.com/news/articles/c8ex2l58en4o"
    zone = "web_unlocker1"

    settings = Settings()

    unlocker = Unlocker(
        api_key=settings.bright_data_api_key,
        zone=zone,
    )

    result = await unlocker.unlock(url)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
