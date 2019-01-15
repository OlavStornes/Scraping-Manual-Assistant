# Scraping Manual Assistant

# Intro
Scraping Manual Assistant (Abbreviated to ScrapingManAss) is a video game manual downloader. 

# Design
ScrapingManass is designed with two modules:

The first part is the database-populator. It utillizes `selenium` to scrape [gamesdatabase.org](http://gamesdatabase.org). Here it finds information regarding the games.

The other part is the manual-downloader. With the records made in the first module, this module aquires, sanitizes and converts it into formatted request urls, attempts to download on a given url and saves the result as a pdf.

# Usage

* `--help -h` : Shows the help menu
* `--list -s` : Show a list of all systems and their corresponding ID
* `--scrapedatabase -s` : Populate the database for taget system(s)
* `--download -d` : Download manuals for games present in the database
* `--both -b` : Activate both the scraper and the downloader 
* `--yes -y` : Skips the confirmation on which systems are targeted


## Arguments
The options -s, -d and -b accepts an arbitrary amount of numbers, so for instance, if you want to scrape several systems, just add the system ID (given from either watching `systems.json` or launching the script with `-l`)

ScrapingManAss also supports dashes between numbers as a range selector (`x-y`) 

### Example:

* `python ./scrapingmanass.py -l` -> Show all the systems with their id's
* `python ./scrapingmanass.py -s 1 2 3 4 5` -> Populate the database with entries from systems 1 to 5 
*  `python ./scrapingmanass.py -b 1-25` -> Populate the database AND download the manuals from systems 1 to 25

# Requirements
The packages used in this project is mentioned in `requirements.txt`.

* [`Selenium`](https://www.seleniumhq.org/) is needed to scrape the webpages.
* `Sqlite3` for the database  

## Apply all packages for easy start:
```pip install -r requirements.txt```
