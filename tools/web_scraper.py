import requests
from bs4 import BeautifulSoup


class WebScraper:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def scrape(self, url: str) -> None | dict:

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            page_title = soup.title.string.strip() if soup.title else "Unknown"

            paragraphs = soup.find_all("p")

            text = " ".join(p.get_text() for p in paragraphs)

            return {
                "text": text.strip(),
                "title": page_title
}

        except Exception as e:
            print("Scraping error:", e)
            return None