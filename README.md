# Scraping Manual Assistant

# Usage

* `--help -h` : Shows the help menu
* `--list -s` : Show a list of all systems and their corresponding ID
* `--scrapedatabase -s` : Populate the database for taget system(s)
* `--download -d` : Download manuals for games present in the database
* `--both -b` : Activate both the scraper and the downloader 
* `--yes -y` : Skips the confirmation on which systems are targeted


## Arguments
The options -s, -d and -b accepts an arbitrary amount of numbers, so for instance, if you want to scrape several systems, just add the system ID (given from either watching `systems.json` or launching the script with `-l`)

### Example:

* `python ./scrapingmanass.py -l` -> Show all the systems with their id's
* `python ./scrapingmanass.py -s 1 2 3 4 5` -> Populate the database with entries from systems 1 to 5  