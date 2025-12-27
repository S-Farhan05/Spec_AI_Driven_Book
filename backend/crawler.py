"""
Docusaurus crawler implementation for the Documentation Ingestion Pipeline
"""
import asyncio
import time
import re
import hashlib
from typing import List, Set, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import logging

from config import Config
from utils import (
    retry_with_exponential_backoff,
    validate_url,
    normalize_url,
    is_valid_docusaurus_url
)
from models import CrawledPage


logger = logging.getLogger(__name__)


class DocusaurusCrawler:
    """Docusaurus crawler class with configurable parameters"""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.base_url = self.config.get('base_url', '')
        self.max_depth = self.config.get('max_depth', Config.CRAWLER_MAX_DEPTH)
        self.delay_between_requests = self.config.get('delay_between_requests', Config.CRAWLER_DELAY_BETWEEN_REQUESTS)
        self.timeout = self.config.get('timeout', Config.CRAWLER_TIMEOUT)
        self.user_agent = self.config.get('user_agent', Config.CRAWLER_USER_AGENT)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})

        # Track visited URLs to avoid infinite loops
        self.visited_urls: Set[str] = set()
        self.crawled_pages: List[CrawledPage] = []

    @retry_with_exponential_backoff(
        max_retries=3,
        exceptions=(requests.RequestException, ConnectionError)
    )
    def fetch_page(self, url: str) -> Tuple[Optional[str], int]:
        """
        Fetch a single page and return its content and status code
        """
        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
                headers={'User-Agent': self.user_agent}
            )
            return response.text, response.status_code
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None, 0

    def extract_links(self, html_content: str, base_url: str) -> List[str]:
        """
        Extract all valid links from the HTML content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()

        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(base_url, href)

            # Only include URLs that are under the base URL domain
            if self.is_valid_internal_link(absolute_url):
                # Additional check to exclude tag URLs
                if '/docs/tags' in absolute_url and absolute_url != f"{self.base_url}/docs/tags":
                    continue  # Skip tag URLs
                links.add(absolute_url)

        return list(links)

    def is_valid_internal_link(self, url: str) -> bool:
        """
        Check if a URL is a valid internal link for the current crawl
        """
        if not validate_url(url):
            return False

        parsed_url = urlparse(url)
        base_parsed_url = urlparse(self.base_url)

        # Check if the URL is under the same domain as the base URL
        if parsed_url.netloc != base_parsed_url.netloc:
            return False

        # Exclude certain file types
        excluded_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe', '.doc', '.docx']
        if any(url.lower().endswith(ext) for ext in excluded_extensions):
            return False

        # Exclude tag URLs to prevent crawling individual tag pages
        if '/docs/tags' in url and url != f"{self.base_url}/docs/tags":
            return False

        return True

    def extract_content_from_html(self, html_content: str, url: str) -> Tuple[str, str]:
        """
        Extract clean text content and title from HTML
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string.strip()
        elif soup.find('h1'):
            title = soup.find('h1').get_text().strip()

        # Extract main content - try to focus on content areas typical for documentation
        content_selectors = [
            'main', 'article', '.main-wrapper', '.docMainContainer',
            '.container', '.content', '.documentation', '.docs-content',
            '.markdown', '.doc-content', '[role="main"]'
        ]

        content = ""
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text(separator=' ', strip=True)
                break

        # If no specific content area found, get all text
        if not content:
            content = soup.get_text(separator=' ', strip=True)

        # Clean up excessive whitespace
        content = re.sub(r'\s+', ' ', content).strip()

        return content, title

    def extract_document_structure(self, url: str) -> Tuple[str, str]:
        """
        Extract module and section information from URL
        """
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]

        if len(path_parts) >= 2:
            module = path_parts[0]
            section = path_parts[1] if len(path_parts) > 1 else path_parts[0]
        elif len(path_parts) == 1:
            module = path_parts[0]
            section = path_parts[0]
        else:
            module = "root"
            section = "index"

        return module, section

    def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Parse sitemap.xml to discover all documentation pages
        """
        try:
            content, status = self.fetch_page(sitemap_url)
            if status != 200 or not content:
                logger.warning(f"Could not fetch sitemap: {sitemap_url}")
                return []

            soup = BeautifulSoup(content, 'xml')  # Use XML parser for sitemap
            urls = []

            for loc in soup.find_all('loc'):
                url = loc.text.strip()
                if self.is_valid_internal_link(url):
                    # Additional check to exclude tag URLs during sitemap parsing
                    if '/docs/tags' in url and url != f"{self.base_url}/docs/tags":
                        continue  # Skip tag URLs
                    urls.append(url)

            logger.info(f"Discovered {len(urls)} URLs from sitemap")
            return urls
        except Exception as e:
            logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
            return []

    def crawl_from_sitemap(self) -> List[CrawledPage]:
        """
        Crawl all pages discovered from sitemap
        """
        sitemap_url = urljoin(self.base_url, 'sitemap.xml')
        urls = self.parse_sitemap(sitemap_url)

        if not urls:
            logger.info("No URLs found in sitemap, falling back to recursive crawling")
            return self.recursive_crawl([self.base_url], 0)

        crawled_pages = []
        for url in urls:
            if url not in self.visited_urls:
                page = self.crawl_single_page(url)
                if page:
                    crawled_pages.append(page)
                    self.visited_urls.add(url)
                    time.sleep(self.delay_between_requests)  # Be respectful to the server

        return crawled_pages

    def recursive_crawl(self, urls: List[str], current_depth: int) -> List[CrawledPage]:
        """
        Recursively crawl from a list of URLs up to max depth
        """
        if current_depth >= self.max_depth:
            logger.info(f"Reached max depth of {self.max_depth}, stopping recursion")
            return []

        crawled_pages = []

        for url in urls:
            # Skip tag URLs to prevent crawling individual tag pages
            if '/docs/tags' in url and url != f"{self.base_url}/docs/tags":
                continue  # Skip tag URLs

            if url in self.visited_urls:
                continue

            page = self.crawl_single_page(url)
            if page:
                crawled_pages.append(page)
                self.visited_urls.add(url)

                # Extract links from the page and continue crawling if under max depth
                if current_depth < self.max_depth - 1:
                    new_pages = self.recursive_crawl(page.links, current_depth + 1)
                    crawled_pages.extend(new_pages)

                time.sleep(self.delay_between_requests)  # Be respectful to the server

        return crawled_pages

    def crawl_single_page(self, url: str) -> Optional[CrawledPage]:
        """
        Crawl a single page and return a CrawledPage object
        """
        logger.info(f"Crawling: {url}")

        content, status_code = self.fetch_page(url)
        if not content or status_code != 200:
            logger.warning(f"Failed to crawl {url}, status: {status_code}")
            return None

        extracted_content, title = self.extract_content_from_html(content, url)
        module, section = self.extract_document_structure(url)
        links = self.extract_links(content, url)

        page_id = f"page_{hashlib.md5(url.encode()).hexdigest()[:12]}_{int(time.time())}"
        crawled_page = CrawledPage(
            page_id=page_id,
            url=url,
            title=title,
            content=extracted_content,
            module=module,
            section=section,
            links=links,
            status_code=status_code
        )

        logger.info(f"Successfully crawled: {url} ({len(extracted_content)} chars)")
        return crawled_page

    def crawl(self) -> List[CrawledPage]:
        """
        Main crawl method that starts the crawling process
        """
        logger.info(f"Starting crawl of {self.base_url} with max depth {self.max_depth}")

        # First, try to crawl from sitemap
        self.crawled_pages = self.crawl_from_sitemap()

        logger.info(f"Crawl completed. Total pages crawled: {len(self.crawled_pages)}")
        return self.crawled_pages