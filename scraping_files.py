import os


PATH = "data/"
CATEGORIES = [r"crypto", r"active", r"gainers", r"losers"]


def download_page(url: str) -> str:
    """
    # This function receives an url address and returns a string with the html file
    :param url: string with an url address
    :return: string with the list
    """
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return web_content


def main():
    for category in CATEGORIES:
        files = os.listdir(PATH+category)
        print(files)



if __name__ == '__main__':
    main()
