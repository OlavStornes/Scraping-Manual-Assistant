import sys
import argparse
import json
import database as data
import tablescraper as ts
import downloader as dl


class ArgHandler():
    def __init__(self):
        self.db = data.db
        self.models = {
            "System": data.System,
            "Game": data.Game
            }

    def handle_args(self):

        self.parser = argparse.ArgumentParser()

        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            "-l", "--list",
            help="Lists all available systems and their number code",
            action="store_true"
        )
        group.add_argument(
            "-d", "--download",
            help="Download the manuals for one or multiple systems",
            nargs='+',
            type=str
        )
        group.add_argument(
            "-s", "--scrapedatabase",
            help="Download the database for one or multiple systems",
            nargs='+',
            type=str
        )
        group.add_argument(
            "-b", "--both",
            help="Download both the database and scrape the \
                    manual for one or multiple systems",
            nargs='+',
            type=str
        )


    def showlist(self):
        for system in self.models['System'].select():
            print(str(system.sys_id) + "\t" + system.name)

    def downloadmanual(self, args):
        query = data.System.select().where(data.System.sys_id.in_(args))

        for entry in query:

            mandownloader = dl.Manualdownloader(entry, self.db, self.models['Game'])
            mandownloader.main()

    def scrapedatabase(self, args):
        query = data.System.select().where(data.System.sys_id.in_(args))

        for entry in query:
            scraper = ts.Scrapie(entry, self.db, self.models['Game'])
            scraper.run()

    def scrape_and_download(self, args):

        self.scrapedatabase(args)
        self.downloadmanual(args)

    def main(self):
        self.handle_args()

        args = self.parser.parse_args()

        if (args.list):
            # Show all systems
            self.showlist()
        elif (args.download):
            # Activate downloader.py
            self.downloadmanual(args.download)

        elif (args.scrapedatabase):
            # Activate tablescraper.py
            self.scrapedatabase(args.scrapedatabase)

        elif (args.both):
            # Do both
            self.scrape_and_download()

        # Avoid starting a nonexistent handler
        else:
            self.parser.print_help()
            sys.exit(2)


if __name__ == "__main__":
    x = ArgHandler()
    x.main()
