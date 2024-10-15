import asyncio
import json
from math import ceil
from typing import Any

import aiohttp


urls = [
    "https://example.com",
    "https://httpbin.org/status/500",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/422",
    "https://nonexistent.url",
    "https://nonexistent.url",
]


async def get_status(session: aiohttp.ClientSession, url: str, s: asyncio.Semaphore) -> dict[str, Any]:
    async with s:
        try:
            async with session.get(url) as resp:
                value = {
                    "url": url,
                    "status_code": resp.status,
                }
                return value
        except:
            return {"url": url, "status_code": 0,}


def limit_coros(urls: list[str], limit: int):
    start = 0
    end = limit

    cycles_count = ceil(len(urls) / limit)

    for _ in range(cycles_count):
        yield urls[start:end]
        start += limit
        end += limit


async def fetch_urls(urls: list[str], file_path: str, limit: int) -> None:
    s = asyncio.Semaphore(limit)
    results = []

    async with aiohttp.ClientSession() as session:
        for batch in limit_coros(urls, 5):
            for result in await asyncio.gather(*[get_status(session, url, s) for url in batch], return_exceptions=True):
                results.append(result)

    with open(file_path, "w") as resultfile:
        for item in results:
            resultfile.write(json.dumps(item) + "\n")


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl', 5))
