import csv
from scraping_tools import *
from datetime import date
import argparse
from config import *
STOCK_URLS = "data_urls.csv"
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']


def calc_periods(from_date):
    min_date = date.fromisoformat('1970-01-01')
    duration1 = from_date-min_date
    period1_sec = int(duration1.total_seconds())
    now = date.today()
    duration2 = now-min_date
    period2_sec = int(duration2.total_seconds())
    return period1_sec, period2_sec


def calc_url_by_from_date(url, period1_sec, period2_sec):
    prefix = url.split('?', 1)[0] + '?'
    periods = 'period1=' + str(period1_sec) + '&period2=' + str(period2_sec)
    suffix = '&' + url.split('&', 2)[2]
    return prefix+periods+suffix


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
    :return: Dict of the useful information from the soup {'Date': 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'}
    """
    data_table = soup.find('table').find('tbody')  # TODO get the headers for the columns from the top of the table
    rows = data_table.find_all('tr')
    stock_data = {}
    for row in rows:
        items = row.find_all('span')
        date = date_str_to_datetime(items[0].text)
        row_data = [float(item.text.replace(',', '')) for item in items[1:]]
        stock_data[date] = row_data
    return stock_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument_group(title='required')
    parser.add_argument('-d', required=True, action='store', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                        help="scrap from this date", dest='from_date')
    parser.add_argument('-sn', required=False, action='store', type=str, help="name of stock to scrap",
                        dest='stock_name')
    args = parser.parse_args()
    period1_sec, period2_sec = calc_periods(args.from_date.date())
    urls = read_urls_files(STOCK_URLS)
    if args.stock_name:
        stock_url = next(stock for stock in urls if stock[0] == args.stock_name)
        urls = [stock_url]
        if not stock_url:
            print('stock doesnt exist, try another one')
            return

    for url in urls:
        stock = url[0]
        stock_by_date_url = calc_url_by_from_date(url[1], period1_sec, period2_sec)
        print("Making {} soup".format(stock))
        soup = make_soup_scrolling(stock_by_date_url, show_year=True)

        if soup is None:
            continue
        info = get_site_info(soup)
        print(info)


if __name__ == '__main__':
    main()
