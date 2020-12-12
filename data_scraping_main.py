import csv
from scraping_tools import *
import datetime
import argparse
HEADERS = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']


def calc_periods(from_date=datetime.date.today() - datetime.timedelta(days=365)):
    """This function takes the date to scrap from for the user and return period1 and period2 so it's ready to insert
        inside the url"""
    min_date = datetime.date.fromisoformat('1970-01-01')
    duration1 = from_date-min_date
    period1_sec = int(duration1.total_seconds())
    duration2 = datetime.date.today()-min_date
    period2_sec = int(duration2.total_seconds())
    return period1_sec, period2_sec


def calc_url_by_from_date(url, period1_sec, period2_sec):
    """This function takes the url and the start and ens periods and insert them in the relevant place in the url """
    prefix = url.split('history?', 1)[0] + 'history?'
    periods = 'period1=' + str(period1_sec) + '&period2=' + str(period2_sec)
    suffix = '&' + url.split('&', 2)[2]
    return prefix+periods+suffix


def get_stocks_urls(db_name) -> list:
    """
    # This function gets the basic url for each stock. It reads the stocks and url from the database
    :return: list for the stocks name and urls [(stock1, stock1_url), (stock1, stock1_url), ...]
    """
    con = connect_to_mysql(db_name)
    cursor = con.cursor()
    cursor.execute(f"USE {db_name};")
    quarry = "SELECT * FROM stock_info;"
    cursor.execute(quarry)
    stock_urls = list(cursor)
    return stock_urls


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


def get_stock_history(stock_url, period1_sec, period2_sec):
    stock = stock_url[0]
    stock_by_date_url = calc_url_by_from_date(stock_url[1], period1_sec, period2_sec)
    # print("Making {} soup".format(stock))
    soup = make_soup_scrolling(stock_by_date_url, show_date=False)
    if soup is None:
        return
    info = get_site_info(soup)
    for date in info:
        values = list(info[date])
        while len(values) != 6:
            values.append('NULL')
        add_query = f"INSERT INTO stock_price (date, stock_name, open_price, high_price, low_price, close_price, " \
                    f"adj_close_price, volume) VALUES(DATE '{date.strftime('%Y-%m-%d')}','{stock}', {values[0]}, " \
                    f"{values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]});"
        con = connect_to_mysql()
        cursor = con.cursor()
        cursor.execute(f"USE {db_name};")
        try:
            cursor.execute(add_query)
        except connector.errors.IntegrityError:
            pass
        con.commit()
        print(f"finished scrapping for {stock}")


def main():
    """ take 2 inputs from the user, one is date to scrap from and the other is stock name/all
        then, calling calc_periods() and calc_url_by_from_date() to scrap the relevant urls"""
    parser = argparse.ArgumentParser()
    parser.add_argument_group(title='required')
    parser.add_argument('-d', required=False, action='store', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                        help="scrap from this date", dest='from_date')
    parser.add_argument('-sn', required=False, action='store', type=str, help="name of stock to scrap",
                        dest='stock_name')
    args = parser.parse_args()
    if args.from_date:
        period1_sec, period2_sec = calc_periods(args.from_date.date())
    else:
        period1_sec, period2_sec = calc_periods()
    stocks_urls = get_stocks_urls(db_name)
    if args.stock_name:
        stock_url = next(stock for stock in stocks_urls if stock[0] == args.stock_name)
        stocks_urls = [stock_url]
        if not stock_url:
            print('stock doesnt exist, try another one')
            return
    for stock_url in stocks_urls:
        print(f"getting history of: {stock_url[0]}")
        x = threading.Thread(target=get_stock_history, args=(stock_url, period1_sec, period2_sec))
        x.start()


if __name__ == '__main__':
    main()
