import urllib.error
import urllib.parse
import urllib.request
import csv

URL = r"https://finance.yahoo.com/cryptocurrencies?offset=0&count=100"



def download_page(url):
    """
    # This function receives an url address and returns a string with the html file
    :param url: string with an url address
    :return: string with the list
    """
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return web_content


def write_to_file(web_string, web_title):
    """
    This function  gets a string of html file and writes it into a local file with the date
    :param input_list: String
    :return True/False weather the input is integers separated by spaces
    """
    if type(input_list) != str:
        return False
    for element in input_list.split(" "):
        if len(element) > 0:
            if element[0] == "-":
                element = element[1:]
        if not element.isnumeric():
            return False
    return True


def main():

    url = URL
    web_string = download_page(url)
    write_to_file(web_string)
    with open('page.html', 'wb') as file:
        file.write(web_string)



if __name__ == '__main__':
    main()
