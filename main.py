import urllib
import urllib.error
import urllib.request
import csv
import asyncio
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, file_name) -> None:
        self.csv_file = 'infos.csv'
        self.base_url = 'http://books.toscrape.com/catalogue/'
        self.url = 'http://books.toscrape.com/catalogue/page-1.html'
        with open(file_name, 'w', -1, 'utf8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Asset'])

    def run(self):
        response = self.collect()
        if response is None:
            return
        
        global parsed
        parsed = BeautifulSoup(response, 'html.parser')
        self.parse()
        self.next()

    def collect(self) -> None | str:
        try:
            with urllib.request.urlopen(self.url) as response:
                return response.read()
        except (urllib.error.URLError, urllib.error.HTTPError):
            return None
    
    def parse(self):
        global parsed
        with open(self.csv_file, 'a', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            articles = parsed.find_all('article', class_='product_pod')
            for article in articles:
                title = article.h3.a['title']
                image = f'http://books.toscrape.com/{article.find("a").img["src"]}'
                price = article.find('p', class_='price_color').text
                writer.writerow([title, price, image])

    def next(self):
        global parsed
        button = parsed.find('li', class_='next')
        url = button.a['href'] if button else None

        if url:
            self.url = self.base_url + url
            self.run()

async def main():
    scraper = Scraper('infos.csv')
    scraper.run()

asyncio.run(main())