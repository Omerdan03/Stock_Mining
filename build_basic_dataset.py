from scraping_tools import *
from selenium import webdriver
import mysql.connector as connector

MAIN_URL = "https://finance.yahoo.com"

def get_stocks_tags(yahoo_main) -> list:
    """
    This function receives the main url og yahoo finance and returns a list with BeautifulSoup objects with the items
     inside the top slider
    :param yahoo_main:
    :return:
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(yahoo_main)
    financial_header = browser.find_element_by_id('Lead-3-FinanceHeader-Proxy')
    next_stock_button = financial_header.find_elements_by_tag_name('button')[1]
    while next_stock_button.is_enabled():
        next_stock_button.click()
    main_soup = BeautifulSoup(browser.page_source, features="lxml")
    slider = main_soup.find('div', {'id': 'YDC-Lead'})
    stocks = slider.find_all('li')
    return stocks


def get_stock_url(stock, name):
    """
    This function receives a beautiful soup tag of a stock and writes it's history URL in the DB
    :type name: object
    :param stock:
    :return: the stock url
    """
    con = connect_to_mysql()
    cursor = con.cursor()
    cursor.execute(f"USE {db_name};")
    url = MAIN_URL + stock.find('a').attrs['href']
    stock_soup = make_soup(url)
    opt = stock_soup.find('div', {'id': 'quote-nav'})
    find_history_page = False
    for tab in opt.find_all('li'):
        if tab.find('span').getText() == 'Historical Data':
            full_history_url = MAIN_URL + tab.find('a').attrs['href'].split('p=')[0] + \
                               'period1=1574968152&period2=1606590552&interval=1d&filter=history&frequency=' \
                               '1d&includeAdjustedClose=true'
            find_history_page = True
    if not find_history_page:
        print(f" could not find history page for {name}")
        return -1
    add_query = f"INSERT INTO stock_info (stock_name, url) VALUES('{name}', '{full_history_url}');"
    try:
        cursor.execute(add_query)
    except connector.errors.IntegrityError:
        del_query = f"DELETE FROM stocks_db.stock_info WHERE stock_name = '{name}';"
        cursor.execute(del_query)
        cursor.execute(add_query)
    con.commit()


def main():
    yahoo_main = MAIN_URL
    con = connect_to_mysql()
    cursor = con.cursor()
    cursor.execute(f"USE {db_name};")
    stocks = get_stocks_tags(yahoo_main)
    stocks_names = []
    for stock in stocks:
        stocks_names.append(stock.attrs['aria-label'])
    print(f'stocks: {stocks_names}')
    for name, stock in zip(stocks_names, stocks):
        print(f"writing index of {name}")
        x = threading.Thread(target=get_stock_url, args=(stock, name))
        x.start()


if __name__ == '__main__':
    main()
