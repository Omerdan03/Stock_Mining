import csv
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import time

STOCK_URLS = "data_urls.csv"
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
MAX_SCROLLING = 40
MAX_YEAR = 2000


def get_urls(url_input) -> list:
    """
    # This function read the url_index file and return a list of tuples with the stock name and url
    :return: list for the stocks name and urls [(stock1, stock1_url), (stock1, stock1_url), ...]
    """
    stock_index = []
    with open(url_input, newline='') as file:
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
        reader = csv.reader(file, dialect)
        for row in reader:
            stock_index.append((row[0], row[1]))
    return stock_index[1:]


def make_soup(url: str, stock_name) -> BeautifulSoup:
    """
    This function gets a url of stocks and returns BeautifulSoup object of that web
    :param url: a url of a web page
    :param stock_name: The name of the current stock
    :return: BeautifulSoup Object of the file
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    year = get_year(BeautifulSoup(driver.page_source, "html.parser"))
    while year > MAX_YEAR:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            time.sleep(1)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height
        year = get_year(BeautifulSoup(driver.page_source, "html.parser"))
        print("Reached {} of {} data".format(year, stock_name))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    return soup


def get_year(soup: BeautifulSoup) -> int:
    """
    This function gets a soup object from Yahoo page and return the last year it has data inside it
    :param soup: A soup object from Yahoo page
    :return:
    """
    data_table = soup.find('table').find('tbody')
    row = data_table.find_all('tr')[-1]
    date_item = row.find('span')
    date = date_str_to_datetime(date_item.text)
    return date.year





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
        for item in items[1:]:
            row_data.append(float(item.text.replace(',', '')))

        stock_data.append(row_data)
    return stock_data


def main():
    urls = get_urls(STOCK_URLS)
    soups_list = {}
    for url in urls[:]:
        stock = url[0]
        print("Making {} soup".format(stock))
        soup = make_soup(url[1], stock)
        soups_list[stock] = soup
        info = get_site_info(soup)
        print(info)

        #  TODO: add tests
        #  TODO: save data and get deltas from last run


if __name__ == '__main__':
    main()
