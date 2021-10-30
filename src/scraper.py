import requests 
import json 
from time import sleep
import hashlib


class Scraper:
    def __init__(self):
        self.headers = {
            'authority': 'www.doximity.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }        

    def scrape(self, url):
        # scrape the page using requests
        print("Scraping {}".format(url))
        r = requests.get(url, headers=self.headers)
        # check if page was blocked (Usually 503)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page {} was blocked by Amazon. Please try using better proxies".format(url))
            else:
                print("Page {} must have been blocked by Amazon as the status code was {}".format(url,r.status_code))
            return None

        # pass the HTML of the page 
        return r.text


def run_scraper():
    # Specialties --> https://www.doximity.com/directory/physicians
    # MichelleHanjani(Hanjani)GalantMD Dermatology • Redwood City, CA
    url = "https://www.doximity.com/pub/michelle-galant-md"
    fn = 'logs/{}.html'.format(hashlib.md5(url.encode('utf-8')).hexdigest())
    scraper = Scraper()
    with open(fn,'wb') as outfile:
        data = scraper.scrape(url) 
        if data:
            outfile.write(data.encode('utf8'))

run_scraper()
