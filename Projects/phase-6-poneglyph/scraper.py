"""One Piece wiki scraper — fetches and parses pages from the Fandom wiki.

Why a scraper instead of a static dataset:
- Real-world RAG systems ingest live data from APIs or websites
- You learn to handle real-world HTML (messy, inconsistent)
- You can scrape any wiki page, not just the curated seed list

The scraper:
1. Fetches HTML from onepiece.fandom.com/wiki/{title}
2. Parses the main content area with BeautifulSoup
3. Extracts text from paragraphs, lists, and section headings
4. Returns structured documents with metadata (title, source URL, categories)
"""

import json
import time
from pathlib import Path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from config import CACHE_DIR, SCRAPER_DELAY, WIKI_BASE_URL, SEED_PAGES


def _fetch_html(title: str) -> Optional[str]:
    """Fetch a wiki page HTML. Caches to disk to avoid re-scraping."""
    cache_file = CACHE_DIR / f"{title.replace('/', '_')}.html"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    url = f"{WIKI_BASE_URL}/{title}"
    headers = {
        "User-Agent": "PoneglyphReader/1.0 (RAG educational project; contact@example.com)",
        "Accept": "text/html,application/xhtml+xml",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        # Cache raw HTML
        cache_file.write_text(resp.text, encoding="utf-8")
        time.sleep(SCRAPER_DELAY)
        return resp.text
    except requests.RequestException as e:
        print(f"  [WARN] Failed to fetch '{title}': {e}")
        return None


def _parse_wiki_content(html: str) -> str:
    """Extract readable text from a Fandom wiki page's main content div."""
    soup = BeautifulSoup(html, "html.parser")

    # Fandom wiki puts content in mw-parser-output
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        return ""

    parts = []
    for element in content_div.find_all(["p", "h2", "h3", "li"], recursive=True):
        tag = element.name
        text = element.get_text(strip=True)
        if not text:
            continue

        # Skip navigation/sidebar elements
        if element.find_parent(["table", "nav", "aside"]):
            continue

        if tag in ("h2", "h3"):
            # Clean section number suffixes like [edit] or [1]
            clean = text.split("[")[0].strip()
            if clean:
                parts.append(f"\n## {clean}")
        elif tag == "li":
            parts.append(f"- {text}")
        elif tag == "p":
            parts.append(text)

    return "\n".join(parts)


def _classify_page(html: str, title: str) -> List[str]:
    """Classify page into categories (character, fruit, location, etc.) based on content."""
    categories = []
    lower = html.lower()
    if "devil fruit" in lower or "gomu" in lower:
        categories.append("devil_fruit")
    if "haki" in lower or "observation" in lower or "conqueror" in lower:
        categories.append("ability")
    if "captain" in lower or "pirate" in lower or "crew" in lower:
        categories.append("character")
    if "island" in lower or "sea" in lower or "ocean" in lower or "grand line" in lower:
        categories.append("location")
    if not categories:
        categories.append("general")
    return categories


def scrape_page(title: str) -> Optional[dict]:
    """Scrape a single One Piece wiki page.

    Returns a dict with keys:
        title       — page title
        source_url  — full URL
        text        — extracted plain text content
        categories  — list of category tags
    """
    html = _fetch_html(title)
    if not html:
        return None

    text = _parse_wiki_content(html)
    if not text:
        print(f"  [WARN] No content extracted from '{title}'")
        return None

    categories = _classify_page(html, title)
    return {
        "title": title.replace("_", " "),
        "source_url": f"{WIKI_BASE_URL}/{title}",
        "text": text,
        "categories": categories,
    }


def scrape_pages(titles: Optional[List[str]] = None) -> List[dict]:
    """Scrape multiple wiki pages. Returns list of document dicts."""
    if titles is None:
        titles = SEED_PAGES
    documents = []
    print(f"Scraping {len(titles)} pages from One Piece wiki...")
    for title in titles:
        print(f"  Fetching: {title}")
        doc = scrape_page(title)
        if doc:
            documents.append(doc)
            print(f"    -> {len(doc['text'])} chars, categories: {doc['categories']}")
    print(f"Scraped {len(documents)}/{len(titles)} pages successfully\n")
    return documents


def list_cached_pages() -> List[str]:
    """List titles of all cached wiki pages."""
    return sorted([f.stem.replace("_", " ") for f in CACHE_DIR.glob("*.html")])


if __name__ == "__main__":
    docs = scrape_pages()
    print(f"\nSample document: {docs[0]['title']}")
    print(f"Text preview: {docs[0]['text'][:200]}...")
