import os
import re


PATH = "data/"
CATEGORIES = [r"crypto"]#, r"active", r"gainers", r"losers"]


def get_price(file_name: str) -> float:
    """
    # This function receives an url address and returns a string with the html file
    :param file_name: string with an url address
    :return: string with the list
    """
    with open(file_name) as file:
        file_string = file.read()
    location = file_string.find('title="Bitcoin USD"')
    stock = re.search("/\w+/", file_name).group()[1:-1]
    print(stock)
    date = file_name[-21:-5]
    print(date)
    print(file_string[location+514:location+523])




def main():
    for category in CATEGORIES:
        files = os.listdir(PATH+category)
        print(files)
        for file in files:
            path = PATH+category+"/"+file
            get_price(path)



if __name__ == '__main__':
    main()
