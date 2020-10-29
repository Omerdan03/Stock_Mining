import urllib.request
import csv
import datetime
import os

URLs = [r"https://finance.yahoo.com/cryptocurrencies?offset=0&count=100",
        r"https://finance.yahoo.com/most-active?offset=0&count=100",
        r"https://finance.yahoo.com/gainers?offset=0&count=100",
        r"https://finance.yahoo.com/losers?offset=0&count=100",]
WEB_NAMEs = [r"crypto", r"active", r"gainers", r"losers"]
CATEGORIES = zip(URLs, WEB_NAMEs)
PATH = "data/"


def download_page(url: str) -> str:
    """
    # This function receives an url address and returns a string with the html file
    :param url: string with an url address
    :return: string with the list
    """
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return web_content


def write_to_file(web_string: str, web_title: str) -> str:
    """
    This function  gets a string of html file and writes it into a local file with the date
    :param web_string: String
    :param web_title: String
    :return True/False weather the input is integers separated by spaces
    """
    folder = PATH+web_title
    if not os.path.exists(folder):
        os.makedirs(str(folder))
    time = str(datetime.datetime.now())[:16].replace(" ", "-")
    file_name = folder+"/"+web_title+"_"+time+".html"
    with open(file_name, 'wb') as file:
        file.write(web_string)


def main():
    if not os.path.exists(PATH):
        os.makedirs(str(PATH))
    print(os.getcwd())
    for category in CATEGORIES:
        url = category[0]
        category_name = category[1]
        print("Computing for: {}".format(category_name))
        web_string = download_page(url)
        write_to_file(web_string, category_name)





if __name__ == '__main__':
    main()
