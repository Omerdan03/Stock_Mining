import csv
from scraping_tools import *

MAIN_URL = "https://finance.yahoo.com"
HISTORICAL_DATA = 3


def get_urls(yahoo_main) -> list:
    """
    # This function receives and main url of yahoo finance and return a list with the urls for the top indexes
    :param yahoo_main: The url for yahoo finance home web page
    :return: list for the stocks name and urls [(stock1, stock1_url), (stock1, stock1_url), ...]
    """
    main_soup = make_soup(yahoo_main, scrolling=False)
    if main_soup is None:
        return []
    urls = []
    slider = main_soup.find('div', {'id': 'YDC-Lead'})  # TODO expend the slider to show all indexes
    stocks = slider.find_all('li')
    for stock in stocks:
        name = stock.attrs['aria-label']
        url = yahoo_main + stock.find('a').attrs['href']
        stock_soup = make_soup(url, scrolling=False)
        if stock_soup is None:
            continue
        opt = stock_soup.find('div', {'id': 'quote-nav'})
        hist = opt.find_all('li')[HISTORICAL_DATA]
        url = yahoo_main + hist.find('a').attrs['href']  # TODO expend the page to show the full history of the index
        urls.append([name, url])

    return urls


def main():
    stocks_urls = get_urls(MAIN_URL)
    with open('data_urls.csv', 'w', newline='') as csv_file:
        stocks = ['Stock_name', 'Yahoo_url']
        writer = csv.DictWriter(csv_file, fieldnames=stocks)
        writer.writeheader()
        for stock in stocks_urls:
            writer.writerow({"Stock_name": stock[0],
                             'Yahoo_url': stock[1]})


if __name__ == '__main__':
    main()

#  TODO Error handling
