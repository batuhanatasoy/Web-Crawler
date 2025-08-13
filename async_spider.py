import sys
import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import tldextract
import time


def actual_domain(url):
    dom = tldextract.extract(url)
    return dom.domain + "." + dom.suffix


async def fetch(client, url, semaphore):
    async with semaphore:
        try:
            resp = await client.get(url, follow_redirects=True, timeout=5)
            resp.raise_for_status()
            return resp
        except httpx.HTTPStatusError as e:
            return e
        except httpx.RequestError:
            return None


async def spider(start_url, file):
    visited = set()
    queued = set()
    queue = deque([start_url])
    queued.add(start_url)
    base_domain = actual_domain(start_url)

    headers = {"User-Agent": "MyAsyncCrawler/1.0"}
    semaphore = asyncio.Semaphore(10)

    with open(file, "w", encoding="utf-8") as success_file, \
         open("async_Errors.txt", "w", encoding="utf-8") as error_file:

        async with httpx.AsyncClient(headers=headers) as client:
            while queue:
                batch_size = min(10, len(queue))
                batch = [queue.popleft() for a in range(batch_size)]

                tasks = [fetch(client, link, semaphore) for link in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for link, result in zip(batch, results):
                    if link in visited:
                        continue

                    visited.add(link)

                    if isinstance(result, httpx.HTTPStatusError):
                        print(f"[{result.response.status_code}] SKIPPING -> {link}")
                        error_file.write(f"[{result.response.status_code}] SKIPPING -> {link}\n")
                        continue
                    elif result is None:
                        print(f"NOT REACHABLE!!! {link}")
                        error_file.write(f"NOT REACHABLE!!! {link}\n")
                        continue

                    if result.history:
                        for r in result.history:
                            print(f"REDIRECTED {r.status_code} {r.url} -> {result.url}")
                            success_file.write(f"REDIRECTED {r.status_code} {r.url} -> {result.url}\n")
                    else:
                        print(link)
                        success_file.write(link + "\n")

                    soup = BeautifulSoup(result.text, "html.parser")
                    for bs_link in soup.find_all("a", href=True):
                        bs_link_url = urljoin(link, bs_link["href"])
                        if actual_domain(bs_link_url) == base_domain and bs_link_url not in visited and bs_link_url not in queued:
                            queue.append(bs_link_url)
                            queued.add(bs_link_url)

                success_file.flush()
                error_file.flush()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\n !!!!!!WRONG FORMAT!!!!!! \n")
        sys.exit(1)

    start_time = time.time()
    start_url = sys.argv[1]

    asyncio.run(spider(start_url, "async_successful_sites.txt"))

    end_time = time.time()
    print(f"total runtime: {end_time - start_time:.2f} seconds") 
