import sys
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import tldextract
import time
done=set()

def actual_domain(url):
    dom=tldextract.extract(url)
    return dom.domain+"."+dom.suffix

def spider(url,file):
    queue = deque([url])
    base_domain= actual_domain(url)
    f= open("sync_Errors.txt","w",encoding="utf-8")
    with open(file,"w",encoding="utf-8") as success_file:
         
            while queue:
                popped_url = queue.popleft()
                if popped_url in done:
                    continue
                done.add(popped_url)
                try:
                
                    html=httpx.get(popped_url,follow_redirects=True ,timeout=5)
                    html.raise_for_status()
                except httpx.HTTPStatusError as e:
                    print(f"[{e.response.status_code}] SKIPPING -> {popped_url}")
                    f.write(f"[{e.response.status_code}] SKIPPING -> {popped_url}\n")
                    f.flush()
                    continue
                except httpx.RequestError:
                    print("NOT REACHABLE!!!",popped_url)
                    f.write(f"NOT REACHABLE!!!{popped_url}\n")
                    f.flush()
                    continue
                if html.history:
                    for r in html.history:
                        print(f" REDİRECTED {r.status_code} {r.url} -> {html.url}")
                        success_file.write(f" REDİRECTED {r.status_code} {r.url} -> {html.url}\n")
                else:
                    print(popped_url)
                    success_file.write(popped_url+"\n")

                soup= BeautifulSoup(html.text,"html.parser")
                for bs_link in soup.find_all("a",href=True):
                    bs_link_url = urljoin(popped_url,bs_link["href"])
                    bs_link_domain=actual_domain(bs_link_url)
                
                    if bs_link_domain == base_domain and bs_link_url not in done:
                        queue.append(bs_link_url)
    f.close()


start_time=time.time()
if __name__ == "__main__":
    if len(sys.argv)!= 2:
        print("\n !!!!!!WRONG FORMAT!!!!!! \n")
        sys.exit(1)

    starting_url=sys.argv[1]

    spider(starting_url,"sync_succesful_sites.txt")
    end_time = time.time()
    runtime = end_time - start_time

    print(f"total runtime: {runtime:.2f} seconds")
