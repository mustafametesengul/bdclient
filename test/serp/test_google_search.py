import asyncio
import json

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from bdclient.serp.google_search import GoogleSearch


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    bright_data_api_key: str = Field(default=...)
    serp_zone: str = Field(default=...)


async def main() -> None:
    settings = Settings()

    keyword = "pizza"

    google_search = GoogleSearch(
        api_key=settings.bright_data_api_key,
        zone=settings.serp_zone,
    )
    result = await google_search.search(keyword)

    print(json.dumps(json.loads(result), indent=4))


if __name__ == "__main__":
    asyncio.run(main())
