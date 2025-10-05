import asyncio
import random
from typing import Generic, TypeVar

import httpx
from pydantic import BaseModel

from bdclient.scraper.base.polling import Polling

Q = TypeVar("Q", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)


class CollectScraper(Generic[Q, R]):
    dataset_id: str
    query_model: type[Q]
    result_model: type[R]

    def __init__(
        self,
        api_key: str,
        include_errors: bool = True,
        limit_per_input: int | None = None,
        polling: Polling | None = None,
        timeout: float = 60.0,
    ) -> None:
        self._url = "https://api.brightdata.com/datasets/v3/trigger"

        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        self._params = {
            "dataset_id": f"{self.dataset_id}",
        }
        if include_errors:
            self._params["include_errors"] = "true"
        if limit_per_input is not None:
            self._params["limit_per_input"] = str(limit_per_input)

        self._snapshot_headers = {
            "Authorization": f"Bearer {api_key}",
        }
        self._snapshot_params = {
            "format": "json",
        }

        if polling is None:
            self._polling = Polling()
        else:
            self._polling = polling

        self._timeout = timeout

    async def scrape(self, queries: list[Q]) -> list[R]:
        snapshot_id = await self.start_scraping(queries)
        results = await self.wait_for_snapshot_results(snapshot_id)
        return results

    async def start_scraping(self, queries: list[Q]) -> str:
        data = [query.model_dump(mode="json") for query in queries]

        async with httpx.AsyncClient(timeout=httpx.Timeout(self._timeout)) as client:
            response = await client.post(
                self._url,
                headers=self._headers,
                params=self._params,
                json=data,
            )
            response.raise_for_status()
            response_json = response.json()

            snapshot_id = str(response_json["snapshot_id"])
            return snapshot_id

    async def wait_for_snapshot_results(self, snapshot_id: str) -> list[R]:
        snapshot_url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"

        async with httpx.AsyncClient(timeout=httpx.Timeout(self._timeout)) as client:
            current_interval = self._polling.poll_interval
            for attempt in range(1, self._polling.max_retries + 1):
                await asyncio.sleep(current_interval)

                response = await client.get(
                    snapshot_url,
                    headers=self._snapshot_headers,
                    params=self._snapshot_params,
                )
                response.raise_for_status()
                response_json = response.json()
                if "status" in response_json:
                    if attempt < self._polling.max_retries:
                        next_interval = current_interval * self._polling.backoff_factor
                        if self._polling.max_poll_interval is not None:
                            next_interval = min(
                                next_interval, self._polling.max_poll_interval
                            )
                        if self._polling.jitter:
                            next_interval += random.uniform(
                                0, float(self._polling.jitter)
                            )
                        current_interval = next_interval
                    continue
                else:
                    return [
                        self.result_model.model_validate(item) for item in response_json
                    ]

            raise RuntimeError(
                f"Failed to retrieve results in time (snapshot {snapshot_id} still processing)."
            )
