import csv
import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import time
"comment2"
STOCK_URLS = "data_urls.csv"
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']


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


def scrolled_html(url, timeout):  # TODO: infinite scrolling
    """

    :param url:
    :param timeout:
    :return:
    """

    scroll_pause_time = timeout
    driver = webdriver.chrome
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


def make_soup(url: str) -> BeautifulSoup:
    """
    This function gets a url of stocks and returns BeautifulSoup object of that web
    :param url: a url of a web page
    :return: BeautifulSoup Object of the file
    """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def date_str_to_datetime(date_str: str) -> datetime:
    """
    This function receives a date in a string format and returns the same date as datetime object
    :param date_str: string of a date
    :return: datetime object of the same date
    """
    date_time_obj = datetime.datetime.strptime(date_str.replace(',', ''), '%b %d %Y')
    return date_time_obj


def get_site_info(soup: BeautifulSoup) -> list:
    """
    This function gets a BeautifulSoup Object and return the useful information from that file
    :param soup: A BeautifulSoup object from one of the stock website.
    :return: List of the useful information from the soup ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    """
    data_table = soup.find('table').find('tbody')
    rows = data_table.find_all('tr')
    stock_data = []
    for row in rows:
        items = row.find_all('span')
        date = date_str_to_datetime(items[0].text)
        row_data = [date]
        for item in items[1:2]:
            row_data.append(float(item.text.replace(',', '')))

        stock_data.append(row_data)
    return stock_data


def main():
    urls = get_urls(STOCK_URLS)
    soups_list = {}
    for url in urls[0:1]:
        stock = url[0]
        print("Making {} soup".format(stock))
        soup = make_soup(url[1])
        soups_list[stock] = soup
        info = get_site_info(soup)
        print(info)

        #  TODO: add tests
        #  TODO: save data and get deltas from last run


if __name__ == '__main__':
    main()
