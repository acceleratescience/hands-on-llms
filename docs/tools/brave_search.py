import json
import os
from typing import List

import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from pydantic import BaseModel, Field

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")


class BraveSearchWrapper(BaseModel):
    """Wrapper around the Brave search engine."""

    api_key: str
    """The API key to use for the Brave search engine."""
    search_kwargs: dict = Field(default_factory=dict)
    """Additional keyword arguments to pass to the search request."""
    base_url: str = "https://api.search.brave.com/res/v1/web/search"
    """The base URL for the Brave search engine."""

    def run(self, query: str) -> str:
        """Query the Brave search engine and return the results as a JSON string.

        Args:
            query: The query to search for.

        Returns: The results as a JSON string.

        """
        web_search_results = self._search_request(query=query)
        final_results = [
            {
                "title": item.get("title"),
                "link": item.get("url"),
                "snippet": " ".join(
                    filter(
                        None, [item.get("description"), *item.get("extra_snippets", [])]
                    )
                ),
            }
            for item in web_search_results
        ]
        return json.dumps(final_results)

    def download_documents(self, query: str) -> List[Document]:
        """Query the Brave search engine and return the results as a list of Documents.

        Args:
            query: The query to search for.

        Returns: The results as a list of Documents.

        """
        results = self._search_request(query)
        return [
            Document(
                page_content=" ".join(
                    filter(
                        None, [item.get("description"), *item.get("extra_snippets", [])]
                    )
                ),
                metadata={"title": item.get("title"), "link": item.get("url")},
            )
            for item in results
        ]

    def _search_request(self, query: str) -> List[dict]:
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json",
        }
        req = requests.PreparedRequest()
        params = {**self.search_kwargs, **{"q": query, "extra_snippets": True}}
        req.prepare_url(self.base_url, params)
        if req.url is None:
            raise ValueError("prepared url is None, this should not happen")

        response = requests.get(req.url, headers=headers)
        if not response.ok:
            raise Exception(f"HTTP error {response.status_code}")

        return response.json().get("web", {}).get("results", [])



def scrape_url(url):
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    
    try:
        # Get the webpage with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
            
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        text = ' '.join(chunk for chunk in lines if chunk)
        
        return text
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error processing webpage: {e}")
        return None
    

brave_client = BraveSearchWrapper(
            api_key=BRAVE_API_KEY,
            search_kwargs={},
        )


def search_brave(query: str, **kwargs):
    response = brave_client.download_documents(query, **kwargs)
    
    # format the response of the top 5 results
    formatted_response = ""
    for result in response[:5]:
        formatted_response += f"{result.metadata['title']}\n"
        formatted_response += f"{result.metadata['link']}\n\n"

    return formatted_response

def scrape_content(url: str):
    return scrape_url(url)