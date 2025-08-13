# Python Web Crawler (Sync & Async)

This repository contains two versions of a simple web crawler:
1. **Synchronous** crawler using `BeautifulSoup` for HTML parsing.
2. **Asynchronous** crawler using `asyncio` and `httpx` for concurrent requests.

Both crawlers extract and follow links within the same domain using `tldextract` for domain matching.

---

## Requirements
- Python 3.13+
- `pip` package manager

---

## Output Files
Each crawler writes its results and errors to separate text files in the project directory:

- `async_Errors.txt` — List of URLs that failed during the asynchronous crawl.
- `async_successful_sites.txt` — List of successfully crawled URLs (async version).
- `sync_Errors.txt` — List of URLs that failed during the synchronous crawl.
- `sync_successful_sites.txt` — List of successfully crawled URLs (sync version).

## Installation
Clone the repository and install the dependencies:
```bash
-git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
-cd YOUR_REPO_NAME
-pip install -r requirements.txt
```


## Usage
### Synchronous Crawler
```bash
python3 sync_crawler.py https://example.com
```
### Asynchronous Crawler
```bash
python3 async_crawler.py https://example.com
```
## Project Structure
 .

├── async_crawler.py      # Asynchronous crawler implementation

├── sync_crawler.py       # Synchronous crawler implementation

├── requirements.txt      # Project dependencies

└── README.md             # Project documentation

## Dependencies
The project uses the following Python libraries:

`beautifulsoup4` - HTML parsing

`tldextract` - Domain extraction

`httpx` - Asynchronous HTTP client
