import re
import requests
from bs4 import BeautifulSoup

class News_spider:
    """
    This class is designed for webcrawling well-known IT news webpages dedicated to CS, cybersecurity, etc.
    """
    def __init__(self):
        """
        spider is a dictonary with the following nested structrure:
            {url: 
                {
                    'info': [list of collected data],
                    'parser': function-parser
                }
            }
        """
        self.spiders = dict()

    def collect_data(self, webpages=None):
        if webpages is None:
            webpages = self.spiders.keys()
        else:
            webpages = set(webpages)
            webpages = webpages.intersection(set(self.spiders.keys()))
            webpages = list(webpages)

        for webpage in webpages:
            self.spiders[webpage]['info'] = self.spiders[webpage]['parser']()
    
    def update_db(self):
        with open('collected_data.txt', 'w') as f:
            for webpage in self.spiders.keys():
                f.write(webpage + '\n')
                # f.write('~NEWS\n')

                for title in self.spiders[webpage]['info']:
                    f.write(title + '\n')

                # f.write('~END\n')

    def get_info(self, webpages=None):
        """
        This function returns a dictionary where |keys| are urls and |values| are lists of collected info
        User can specify required webpages to get appropriate info or not to pass parameters to get all info
        """
        if webpages is None:
            webpages = self.spiders.keys()
        else:
            webpages = set(webpages)
            all_webpages = set(self.spiders.keys())
            
            webpages = list(required_webpages.intersection(all_webpages))

        results = dict()

        for webpage in webpages:
            results[webpage] = self.spiders[webpage]['info']

        return results

    def add_parser(self, url):
        """
        The part where the HTTP GET request is done and Beautiful Soup is created are the same for all target webpages,
        so this function is designed as a decorator
        User have to define only parsing logic according to bs4 capabilities
        """
        def decorator(func):
            def wrapper():
                try:
                    doc = requests.get(url).text
                except requests.exceptions.ConnectionError:
                    return ['ERROR: Cannot collect data due to connection error']
                
                soup = BeautifulSoup(doc, 'lxml')
                
                return func(soup)

            self.spiders[url] = dict()
            self.spiders[url]['parser'] = wrapper
            self.spiders[url]['info']   = []

            return wrapper
        return decorator

news_spider = News_spider()

@news_spider.add_parser('https://veteransec.com')
def vetsec_parse(soup: BeautifulSoup) -> list:
    return [soup.find('article', id=re.compile("^post-")).find('h2').text]

@news_spider.add_parser('https://hackaday.com')
def hackaday_parse(soup: BeautifulSoup) -> list:
    return [soup.find('div', class_='entry-intro').find('h2').text]

@news_spider.add_parser('https://defcon.org')
def defcon_parse(soup: BeautifulSoup) -> list:
    return [title.text for title in soup.find_all('h2')]

@news_spider.add_parser('https://towardsdatascience.com')
def td_parse(soup: BeautifulSoup) -> list:
    return [soup.find('h3').text]

news_spider.collect_data()
news_spider.update_db()
print(news_spider.get_info())




