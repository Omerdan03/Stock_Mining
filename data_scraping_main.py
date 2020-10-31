import csv
import urllib
import requests
from bs4 import BeautifulSoup


def get_urls() -> list:
    """
    # This function read the url_index file and return a list of tuples with the stock name and url
    :return: list for the stocks name and urls [(stock1, stock1_url), (stock1, stock1_url), ...]
    """
    stock_index = []
    with open('data_urls.csv', newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for row in reader:
            stock_index.append((row[0], row[1]))
    return stock_index[1:]


def download_page(url: str) -> str:
    """
    # This function receives an url address and returns a string with the html file
    :param url: string with an url address
    :return: string with the list
    """
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return web_content


def main():
    urls = get_urls()
    soups = []
    for url in urls:
        print("Making {} soup".format(url[0]))
        html = download_page(url[1])
        soup = BeautifulSoup(html, 'lxml')
        soups.append((url[0], soup))




if __name__ == '__main__':
    main()