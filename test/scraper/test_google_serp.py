import asyncio

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from bdclient.scraper.google_serp import CollectByURL, CollectByURLQuery


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    bright_data_api_key: str = Field(default=...)


async def main() -> None:
    settings = Settings()

    query = CollectByURLQuery(keyword="AI")
    scraper = CollectByURL(api_key=settings.bright_data_api_key, limit_per_input=2)

    results = await scraper.scrape([query])
    for result in results:
        print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
