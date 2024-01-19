
import json
from robocorp.actions import action
from robocorp import browser

@action
def search_wikipedia(topic: str) -> str:
    """Search Wikipedia for a topic

    Args:
        topic (str): Topic to search in Wikipedia

    Returns:
        str: First paragraph of the topic wiki page
    """

    browser.configure(browser_engine="chromium", headless=True)
    page = browser.goto("https://wikipedia.org")


    page.fill("#searchInput", f"{topic}")
    page.press("#searchInput", "Enter")

    page.wait_for_selector("#mw-content-text")

    paragraph = page.query_selector("#mw-content-text > div p:not(.mw-empty-elt)")
    content = paragraph.text_content()

    return content