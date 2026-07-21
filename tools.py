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
    
if __name__ == "__main__":
    print(web_search.invoke("what is the recent news of worldcup 2026?"))
