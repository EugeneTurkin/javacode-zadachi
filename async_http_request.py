import asyncio
import json

import aiohttp


urls = [
    "https://example.com",
    "https://httpbin.org/status/500",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/422",
    "https://nonexistent.url",
]


async def producer(queue, urls):
    for url in urls:
        await queue.put(url)


async def consumer(queue, file_path):
    with open(file_path, "a") as f:
        while True:
            url = await queue.get()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        data = {"url": url, "status_code": resp.status,}
            except Exception as e:
                data = {"url": url, "status_code": 0,}
            finally:
                queue.task_done()

            f.write(json.dumps(data) + "\n")


async def main(urls: list[str], file_path: str, limit: int):
    queue = asyncio.Queue()

    produce = asyncio.create_task(producer(queue, urls))
    
    consumers = [asyncio.create_task(consumer(queue, file_path)) for _ in range(limit)]
    
    await produce

    await queue.join()


if __name__ == '__main__':
    from time import time
    ts = time()

    asyncio.run(main(urls, './results.jsonl', 5))

    print(time() - ts)
