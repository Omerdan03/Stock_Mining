import csv
from datetime import date
import argparse
from scraping_tools import *
from config import *
STOCK_URLS = "data_urls.csv"
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']



def calc_periods(from_date):
    
    """This function takes the date to scrap from for the user and return period1 and period2 so it's ready to insert 
    inside the url"""
    
    min_date = date.fromisoformat('1970-01-01')
    duration1 = from_date-min_date
    period1_sec = int(duration1.total_seconds())
    now = date.today()
    duration2 = now-min_date
    period2_sec = int(duration2.total_seconds())
    return period1_sec, period2_sec

def calc_url_by_from_date(url, period1_sec, period2_sec):
    
    """This function takes the url and the start and ens periods and insert them in the relevant place in the url """

    prefix = url.split('?',1)[0] + '?'
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
    """ take 2 inputs from the user, one is date to scrap from and the other is stock name/all
    then, calling calc_periods() and calc_url_by_from_date() to scrap the relevant urls"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument_group(title='required')
    parser.add_argument('-d', required=True, action='store', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="scrap from this date", dest='from_date')
    parser.add_argument('-sn', required=False, action='store', type=str, help="name of stock to scrap", dest='stock_name')
    args = parser.parse_args()
    #args = parser.parse_args(['-d', '2020-11-01'])
    #args = parser.parse_args(['-d', '2020-11-01', '-sn', 'Nasdaq'])
    period1_sec, period2_sec = calc_periods(args.from_date.date())

    urls = read_urls_files(STOCK_URLS)
    if (args.stock_name is not None):
        stock_url = next(x for x in urls if x[0] == args.stock_name)
        urls = [stock_url]
        if stock_url is None:
            print('stock doesnt exist, try another one')
            return

    for url in urls[:]:
        stock = url[0]
        stock_by_date_url = calc_url_by_from_date(url[1], period1_sec, period2_sec)
        print("Making {} soup".format(stock))
        soup = make_soup_scrolling(stock_by_date_url, show_year=True)
        if soup is None:
            continue
        info = get_site_info(soup)
        print(info)

        #  TODO: save data and get deltas from last run
        #  TODO Error handling


if __name__ == '__main__':
    main()
