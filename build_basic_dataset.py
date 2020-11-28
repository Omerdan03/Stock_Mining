from scraping_tools import *
from selenium import webdriver
import mysql.connector as connector

MAIN_URL = "https://finance.yahoo.com"


def load_all_slider_stocks(browser):
    """

    :param browser:
    :return:
    """
    financial_header = browser.find_element_by_id('Lead-3-FinanceHeader-Proxy')
    next_stock_button = financial_header.find_elements_by_tag_name('button')[1]
    while next_stock_button.is_enabled():
        next_stock_button.click()


def get_full_page(yahoo_main) -> list:
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
    load_all_slider_stocks(browser)
    main_soup = BeautifulSoup(browser.page_source, features="lxml")
    slider = main_soup.find('div', {'id': 'YDC-Lead'})
    stocks = slider.find_all('li')
    return stocks


def main():
    yahoo_main = MAIN_URL
    con = connect_to_mysql()
    cursor = con.cursor()
    cursor.execute(f"USE {db_name};")
    stocks = get_full_page(yahoo_main)
    for i, stock in enumerate(stocks):
        name = stock.attrs['aria-label']
        print("writing index of {}\n {} out of {}".format(name, i + 1, len(stocks)))
        url = yahoo_main + stock.find('a').attrs['href']
        stock_soup = make_soup(url)
        opt = stock_soup.find('div', {'id': 'quote-nav'})
        for tab in opt.find_all('li'):
            if tab.find('span').getText() == 'Historical Data':
                full_history_url = yahoo_main + tab.find('a').attrs['href'].split('p=')[0] + \
                                   'period1=1574968152&period2=1606590552&interval=1d&filter=history&frequency=' \
                                   '1d&includeAdjustedClose=true'
                break
        add_query = f"INSERT INTO stock_info (stock_name, url) VALUES('{name}', '{full_history_url}');"
        try:
            cursor.execute(add_query)
        except connector.errors.IntegrityError:
            del_query = f"DELETE FROM stocks_db.stock_info WHERE stock_name = '{name}';"
            cursor.execute(del_query)
            cursor.execute(add_query)
        con.commit()


if __name__ == '__main__':
    main()
