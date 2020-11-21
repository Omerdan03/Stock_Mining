import csv
from selenium.webdriver.common.keys import Keys
from scraping_tools import *
from selenium import webdriver

MAIN_URL = "https://finance.yahoo.com"
HISTORICAL_DATA = 3


def load_all_slider_stocks(browser):
    financial_header = browser.find_element_by_id('Lead-3-FinanceHeader-Proxy')
    next_stock_button = financial_header.find_elements_by_tag_name('button')[1]
    while (next_stock_button.is_enabled()):
        next_stock_button.click()


def get_all_historical_stock_data(browser):
    history_box = browser.find_element_by_id('Col1-1-HistoricalDataTable-Proxy')
    loaded_history = history_box.find_elements_by_tag_name('tr')
    previously_loaded = len(loaded_history)
    while True:
        #scroll down
        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(2)
        loaded_history = history_box.find_elements_by_tag_name('tr')
        if (len(loaded_history) == previously_loaded):
            break
        previously_loaded = len(loaded_history)
    return loaded_history


def get_urls(yahoo_main) -> list:
    """
    # This function receives and main url of yahoo finance and return a list with the urls for the top indexes
    :param yahoo_main: The url for yahoo finance home web page
    :return: list for the stocks name and urls [(stock1, stock1_url), (stock1, stock1_url), ...]
    """

    # try:
    #     element = WebDriverWait(browser, 10).until(
    #         EC.presence_of_element_located((By.ID, "marketsummary-itm-6"))
    #     )
    # finally:
    #     browser.quit()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(yahoo_main)
    load_all_slider_stocks(browser)
    main_soup = BeautifulSoup(browser.page_source, features="lxml")
    urls = []

    slider = main_soup.find('div', {'id': 'YDC-Lead'})  # TODO expend the slider to show all indexes
    stocks = slider.find_all('li')
    for i, stock in enumerate(stocks):
        name = stock.attrs['aria-label']
        print("making index of {}\n {} out of {}".format(name, i+1, len(stocks)))
        url = yahoo_main + stock.find('a').attrs['href']
        stock_soup = make_soup(url, scrolling=False)
        opt = stock_soup.find('div', {'id': 'quote-nav'})
        for tab in opt.find_all('li'):
            if tab.find('span').getText() == 'Historical Data':
                full_history_url = yahoo_main + tab.find('a').attrs['href'].split('p=')[
                    0] + 'period1=-3000000000&period2=3000000000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
                break
        # browser.get(full_history_url)
        # stock_history = get_all_historical_stock_data(browser) #do something with stock history?
        urls.append([name, full_history_url])

    return urls


def main():
    # get the names of stocks in the main page
    # go over each page, load it, and parse it
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
