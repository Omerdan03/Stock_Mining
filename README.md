# Stock_Mining

Stock mining is a python program for scrapping Yahoo finance top indexes along the history and examine trends.
Example stocks are: S&P 500, Dow Jones, NASDAQ etc.

# Installation

In order to run stock mining you will need the following packages installed over basic python 3.x:

beautifullysoup4
selenium

# Usage
First run build_basic_dataset.py for first setup.

Then every time you need to scrape Yahoo run data_scraping_main.py
when running data_scraping_main.py user should insert two parameters:
param1: (-d) date to scrap from ('%Y-%m-%d')
param2: (-sn) the stock name which you would like to scrap the data for. If not given, all stocks will be chosen.
once all desired data has been scraped the user interface will be directly from sql DB. 


# Contributors
This program was build and maintained by Omer Danziger and Barak Beitner as part of \<ITC> Data Science program
