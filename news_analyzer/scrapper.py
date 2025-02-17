from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.async_configs import CacheMode
from crawl4ai.async_crawler_strategy import BrowserConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape(url):
    """
    Scrapes the content of the URL and returns the content in markdown format.
    """
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.6, threshold_type="fixed")
    )
    
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator,
        only_text=True,
        remove_forms=True,
        wait_until="domcontentloaded",
        delay_before_return_html=2.0,
        magic=True, #If True, attempts automatic handling of overlays/popups
        simulate_user=True, #If True, simulate user interactions (mouse moves, clicks) for anti-bot measures.
        override_navigator=True, #If True, attempts automatic handling of overlays/popups.
        ignore_body_visibility=False, #If True, ignore whether the body is visible before proceeding.
        scroll_delay=0.5, #Delay in seconds between scroll steps if scan_full_page is True.
        verbose=True
    )
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=False)) as crawler:
        result = await crawler.arun(url, config=config)
        print("FIT Markdown: ", result.markdown_v2.fit_markdown)
        print("FIT Markdown length: ", len(result.markdown_v2.fit_markdown))
        return result.markdown_v2.fit_markdown
# ...existing code...
