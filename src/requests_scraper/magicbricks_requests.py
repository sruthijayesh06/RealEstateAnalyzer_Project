import csv
import requests
from bs4 import BeautifulSoup

class NoBrokerRequestsScraper:
    def __init__(self):
        self.results = []

    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url)
        print(f" | Status code: {res.status_code}")
        return res

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.select('h2.heading-6 a')

        for a in a_tags:
            title = a.get_text(strip=True)
            href = a.get('href', '')
            link = "https://www.nobroker.in" + href if href.startswith('/') else href

            print(title, "->", link)

            self.results.append({
                "title": title,
                "link": link
            })

    def to_csv(self, filename="nobroker_results.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link"])
            writer.writeheader()
            writer.writerows(self.results)

        print(f"\nSaved {len(self.results)} listings to {filename}")

    def run(self):
        url = (
    "https://www.nobroker.in/property/sale/mumbai/Navi%20Mumbai?"
    "searchParam=W3sibGF0IjoxOS4wMzMwNDg4LCJsb24iOjczLjAyOTY2MjUsInBsYWNlSWQiOiJDaElKclJNZnVQQzU1enNSYWZpRkVXajNFanciLCJwbGFjZU5hbWUiOiJOYXZpIE11bWJhaSJ9XQ=="
    "&radius=2.0&city=mumbai&locality=Navi%20Mumbai"
    "&nbFr=service_page&type=BHK1,BHK2,BHK3,BHK4,BHK4PLUS"
    "&price=0,100000000"
)
        res = self.fetch(url)
        self.parse(res.text)
        self.to_csv()


if __name__ == "__main__":
    scraper = NoBrokerRequestsScraper()
    scraper.run()
