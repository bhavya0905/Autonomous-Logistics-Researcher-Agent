from tools.web_scraper import WebScraper

scraper = WebScraper()

text = scraper.scrape("https://en.wikipedia.org/wiki/Logistics")

print(text[:500])