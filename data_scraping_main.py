import csv
import urllib
import requests
from bs4 import BeautifulSoup


STOCK_URLS = "data_urls.csv"


def get_urls(url_input) -> list:
    """
    # This function read the url_index file and return a list of tuples with the stock name and url
    :return: list for the stocks name and urls [(stock1, stock1_url), (stock1, stock1_url), ...]
    """
    stock_index = []
    with open(url_input, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for row in reader:
            stock_index.append((row[0], row[1]))
    return stock_index[1:]


def make_soup(url: str) -> BeautifulSoup:
    """
    This function gets a url of stocks and returns BeautifulSoup object of that web
    :param url: a url of a web page
    :return: BeautifulSoup Object of the file
    """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def get_site_info(soup: BeautifulSoup) -> list:
    """
    This function gets a BeautifulSoup Object and return the useful information from that file
    :param soup:
    :return:
    """
    data_table = soup.find('table')

    print(data_table)


def main():
    urls = get_urls(STOCK_URLS)
    soups_list = {}
    for url in urls:
        stock = url[0]
        print("Making {} soup".format(stock))
        soup = make_soup(url[1])
        soups_list[stock] = soup
        info = get_site_info(soup)





if __name__ == '__main__':
    main()