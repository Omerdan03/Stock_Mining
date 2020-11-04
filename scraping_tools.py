import csv
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import time


def make_soup(url: str, scrolling=True, dis_year=False) -> BeautifulSoup:
    """
    This function gets a url of stocks and returns BeautifulSoup object of all the information from that web
    :param scrolling: A flag if scrolling is needed in the site
    :param dis_year: A flag for displaying the current year when scrolling
    :param url: a url of a web page
    :return: BeautifulSoup Object of the file
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while scrolling:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            time.sleep(1)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height
        if dis_year:
            year = get_year(BeautifulSoup(driver.page_source, "html.parser"))
            print("Year reached: {}".format(year))
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
