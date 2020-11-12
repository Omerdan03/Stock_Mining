import csv
from scraping_tools import *

STOCK_URLS = "data_urls.csv"
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']


def read_urls_files(url_input) -> list:
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


def get_site_info(soup: BeautifulSoup) -> list:
    """
    This function gets a BeautifulSoup Object and return the useful information from that file
    :param soup: A BeautifulSoup object from one of the stock website.
    :return:List of the useful information from the soup ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    """
    data_table = soup.find('table').find('tbody')  # TODO get the headers for the columns from the top of the table
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
    urls = read_urls_files(STOCK_URLS)
    for url in urls[:]:
        stock = url[0]
        print("Making {} soup".format(stock))
        soup = make_soup(url[1], scrolling=True, show_year=True)
        if soup is None:
            continue
        info = get_site_info(soup)
        print(info)

        #  TODO: save data and get deltas from last run
        #  TODO Error handling


if __name__ == '__main__':
    main()
