from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import mysql.connector as connector
import selenium
import time
from config import *


def make_soup(url: str) -> BeautifulSoup:
    """
    This function gets a url of stocks and returns BeautifulSoup object of all the information from that web
    :param url: a url of a web page
    :return: BeautifulSoup Object of the site
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
    except selenium.common.exceptions.WebDriverException as e:
        print(e)
        return None
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    return soup


def make_soup_scrolling(url: str, show_year=False) -> BeautifulSoup:
    """
    This function gets a url of stocks and returns BeautifulSoup object of all the information from that web
    :param show_year: A flag for displaying the current year when scrolling
    :param url: a url of a web page
    :return: BeautifulSoup Object of the file
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
    except selenium.common.exceptions.WebDriverException as e:
        print(e)
        return None
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            time.sleep(1)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height
        if show_year:
            year = get_year(BeautifulSoup(driver.page_source, "html.parser"))
            print("Year reached: {}".format(year))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    return soup


def get_year(soup: BeautifulSoup) -> int:
    """
    This function gets a soup object from Yahoo page and return the last year it has data inside it
    :param soup: A soup object from Yahoo page
    :return:The year of the last row in the data
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


def connect_to_mysql(db='stocks_db'):
    """
    This function uses the configuration from config.py file and returns a connection the mysql. if stocks_db doesn't
    exists it create one according to stock_prices.sql file.
    :return: a connection at the stacks_db database:
    """
    host, user, password = sql_conf.get_connection_info()
    con = connector.connect(host=host, user=user, password=password)
    cursor = con.cursor()
    cursor.execute("SHOW DATABASES;")
    db_tuples = list(cursor)
    dbs = [db[0] for db in db_tuples]
    if db not in dbs:
        cursor.execute(f"CREATE DATABASE {db}")
        cursor.execute(f"USE {db};")
        with open("stock_prices.sql") as file:
            new_db_command = file.read()
        cursor.execute(new_db_command)
        con = connector.connect(host=host, user=user, password=password)
    return con


def init_db(db='stocks_db'):
    con = connect_to_mysql()
    cursor = con.cursor()
    cursor.execute(f"USE {db};")


