from readability import Document
from bs4 import BeautifulSoup
import requests

class WebScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def scrape(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            # basic validation
            if response.status_code != 200:
                return None

            if "text/html" not in response.headers.get("Content-Type", ""):
                return None

            # extract main content
            doc = Document(response.text)
            title = doc.short_title()
            main_html = doc.summary()

            soup = BeautifulSoup(main_html, "html.parser")

            paragraphs = soup.find_all("p")

            # CLEANING
            cleaned = []
            for p in paragraphs:
                line = p.get_text(strip=True)

                if not line:
                    continue
                if len(line) < 50:
                    continue
                if line.lower().startswith(("read more", "also read", "click here")):
                    continue
                if "cookie" in line.lower():
                    continue

                cleaned.append(line)

            text = " ".join(cleaned)

            # reject low-quality pages
            if len(text) < 300:
                return None

            return {
                "url": url,
                "title": title,
                "text": text
            }

        except Exception as e:
            print("Scraping error:", e)
            return None