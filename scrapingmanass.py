import sys
import argparse
import json
import tablescraper as ts
import downloader as dl


class ArgHandler():

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

    def load_data(self):
        with open('systems.json') as f:
            self.data = json.load(f)

    def showlist(self):
        self.load_data()

        for line in self.data:
            print(line + "\t" + self.data[line])

    def downloadmanual(self, args):
        self.load_data()

        for x in args:
            system = self.data[x]
            mandownloader = dl.Manualdownloader(system)
            mandownloader.main()

    def scrapedatabase(self, args):
        self.load_data()

        for x in args:
            system = self.data[x]
            scraper = ts.Scrapie(system)
            scraper.run()

    def scrape_and_download(self, args):
        self.load_data()


        self.downloadmanual()
        self.scrapedatabase()

    def main(self):
        self.handle_args()

        args = self.parser.parse_args()

        if (args.list):
            # Show all systems
            self.showlist()
        elif (args.download):
            # Activate downloader.py
            self.downloadmanual(args.path)

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
