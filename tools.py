from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool 
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic. Returns Title, URLs and snippets.
    """
    response = tavily.search(query=query, max_results=5)
    results = response.get("results", [])

    out = []

    for result in results:
        title = result.get("title", "Untitled")
        url = result.get("url", "No URL")
        content = result.get("content") or "No snippet available."
        out.append(
            f"Title: {title}\nURL: {url}\nSnippet: {content[:300]}\n"
        )

    return "\n----\n".join(out) if out else "No results found."

    # try:
    #     results = tavily.search(query=query, max_results=5)

    #     if results and len(results) > 0:
    #         return results[0]['url']
    #     else:
    #         return "No results found."
    # except Exception as e:
    #     return f"An error occurred during the web search: {str(e)}"
    
@tool
def scrape_url(url: str) -> str:
    """
    Scrape the content of a given URL and return the text content.
    """
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()  # Remove these tags from the soup
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content[:3000]  # Return first 1000 characters for brevity
    except Exception as e:
        return f"An error occurred while scraping the URL: {str(e)}"

if __name__ == "__main__":
    print(scrape_url.invoke("https://www.espn.com/soccer/match/_/gameId/760517/argentina-spain"))
