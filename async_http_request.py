import aiohttp
import asyncio
import json
from typing import Any


urls = [
    "https://example.com",
    "https://httpbin.org/status/500",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/422",
    "https://nonexistent.url",
]


async def get_status(session: aiohttp.ClientSession, url: str) -> dict[str, Any]:
    try:
        async with session.get(url) as resp:
            value = {
                "url": url,
                "status_code": resp.status,
            }
            return value
    except:
        return {"url": url, "status_code": 0,}



async def fetch_urls(urls: list[str], file_path: str) -> None:

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=3)) as session:
        results = await asyncio.gather(*[get_status(session, url) for url in urls], return_exceptions=True)

    with open(file_path, "w") as resultfile:
        for item in results:
            resultfile.write(json.dumps(item) + "\n")


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
