import requests
from bs4 import BeautifulSoup


class WebScraper:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def scrape(self, url: str):

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            paragraphs = soup.find_all("p")

            text = " ".join(p.get_text() for p in paragraphs)

            return text.strip()

        except Exception as e:
            print("Scraping error:", e)
            return None