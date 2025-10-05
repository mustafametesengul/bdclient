from typing import TypeVar

from pydantic import BaseModel

from bdclient.scraper.base.collect import CollectScraper
from bdclient.scraper.base.polling import Polling

Q = TypeVar("Q", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)


class DiscoveryScraper(CollectScraper[Q, R]):
    discover_by: str

    def __init__(
        self,
        api_key: str,
        include_errors: bool = True,
        discovery_only: bool = False,
        limit_per_input: int | None = None,
        polling: Polling | None = None,
        timeout: float = 60.0,
    ) -> None:
        super().__init__(
            api_key=api_key,
            include_errors=include_errors,
            limit_per_input=limit_per_input,
            polling=polling,
            timeout=timeout,
        )
        self._params["type"] = "discover_new"
        self._params["discover_by"] = self.discover_by
        if discovery_only:
            self._params["discovery_only"] = "true"
