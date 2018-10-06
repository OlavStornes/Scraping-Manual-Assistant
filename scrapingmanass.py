import sys
import argparse
import database as data
import tablescraper as ts
import downloader as dl
import colorama
from termcolor import colored, cprint


class ArgHandler():
    def __init__(self):
        self.db = data.db
        self.models = {
            "System": data.System,
            "Game": data.Game
        }
        colorama.init()


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
        self.parser.add_argument(
            "-y", "--yes",
            help="Ignore the confirmation on the start",
            action="store_true"
        )

    def showlist(self):
        for system in self.models['System'].select():
            print(str(system.sys_id) + "\t" + system.name)

    def downloadmanual(self, args, skip_confirmation):
        query = data.System.select().where(data.System.sys_id.in_(args))

        confirm_string = 'Download the database for one or multiple systems'
        self.confirm_action(query, confirm_string, skip_confirmation)

        for entry in query:

            mandownloader = dl.Manualdownloader(
                entry, self.db, self.models['Game'])
            mandownloader.main()

    def scrapedatabase(self, args, skip_confirmation):
        query = data.System.select().where(data.System.sys_id.in_(args))

        confirm_string = 'Scrape game info from the website'
        self.confirm_action(query, confirm_string, skip_confirmation)

        for entry in query:
            scraper = ts.Scrapie(entry, self.db, self.models['Game'])
            scraper.run()

    def scrape_and_download(self, args, skip_confirmation):
        query = data.System.select().where(data.System.sys_id.in_(args))

        confirm_string = 'Download both the database and scrape the \
                        manual for one or multiple systems"'
        self.confirm_action(query, confirm_string, skip_confirmation)

        self.scrapedatabase(args, True)
        self.downloadmanual(args, True)

    def confirm_action(self, args, confirm_string, skip_confirmation):
        if not skip_confirmation:
            print("You are currently attempting the following:")
            cprint(confirm_string + "\n", 'red')

            # query = data.System.select().where(data.System.sys_id.in_(args))
            for entry in args:
                print(entry.name)

            proceed = input("Do you wish to proceed? y/n: > ")

            if proceed != 'y':
                sys.exit(1)

    def main(self):
        self.handle_args()

        args = self.parser.parse_args()

        skip_confirmation = args.yes

        if (args.list):
            # Show all systems
            self.showlist()
        elif (args.download):
            # Activate downloader.py
            self.downloadmanual(args.download, skip_confirmation)

        elif (args.scrapedatabase):
            # Activate tablescraper.py
            self.scrapedatabase(args.scrapedatabase, skip_confirmation)

        elif (args.both):
            # Do both
            self.scrape_and_download(args.both, skip_confirmation)

        # Avoid starting a nonexistent handler
        else:
            self.parser.print_help()
            sys.exit(2)


if __name__ == "__main__":
    x = ArgHandler()
    x.main()
