import urllib.error
import urllib.request
import csv
from bs4 import BeautifulSoup
from pathlib import Path

class Scraper:
    def __init__(self, file_name: str) -> None:
        self.csv_file = Path(file_name)
        self.base_url = 'http://books.toscrape.com/catalogue/'
        self.url = 'http://books.toscrape.com/catalogue/page-1.html'
        self.csv_file.write_text('', encoding='utf8')
        with self.csv_file.open('w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Asset'])

    def run(self) -> None:
        response = self.collect()
        if response is None:
            return
        
        parsed = BeautifulSoup(response, 'html.parser')
        self.parse(parsed)
        self.next(parsed)

    def collect(self) -> None | bytes:
        try:
            with urllib.request.urlopen(self.url) as response:
                return response.read()
        except (urllib.error.URLError, urllib.error.HTTPError):
            return None
    
    def parse(self, parsed: BeautifulSoup) -> None:
        with self.csv_file.open('a', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            articles = parsed.find_all('article', class_='product_pod')
            for article in articles:
                title = article.h3.a['title']
                image = f"http://books.toscrape.com/{article.find('a').img['src']}"
                price = article.find('p', class_='price_color').text
                writer.writerow([title, price, image])

    def next(self, parsed: BeautifulSoup) -> None:
        button = parsed.find('li', class_='next')
        if button and button.a:
            self.url = self.base_url + button.a['href']
            self.run()

def main() -> None:
    scraper = Scraper('infos.csv')
    scraper.run()

if __name__ == "__main__":
    main()