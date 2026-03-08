from tavily import TavilyClient
from config.settings import get_settings


class SearchTool:

    def __init__(self):
        settings = get_settings()

        self.api_key = settings.TAVILY_API_KEY
        self.client = None

        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)

    def search(self, query: str, max_results: int = 5):

        if not self.client:
            return {
                "status": "Search disabled",
                "reason": "Tavily API key not configured"
            }

        results = self.client.search(
            query=query,
            max_results=max_results
        )

        return results["results"]