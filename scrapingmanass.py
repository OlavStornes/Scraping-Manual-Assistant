import sys
import argparse


class ArgHandler():

    def handle_args(self):

        self.parser = argparse.ArgumentParser()

        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            "-d", "--download",
            help="Download the manuals for one or multiple systems",
            nargs='+',
            type=int
        )
        group.add_argument(
            "-l", "--list",
            help="Lists all available systems and their number code",
            action="store_true"
        )
        group.add_argument(
            "-s", "--scrapedatabase",
            help="Download the database for one or multiple systems",
            nargs='+',
            type=int
        )
        group.add_argument(
            "-b", "--both",
            help="Download both the database and scrape the \
                    manual for one or multiple systems",
            nargs='+',
            type=int
        )

    def showlist(self):
        with open('systems.csv') as f:
            for index, line in enumerate(f):
                print(str(index) + ": \t" + line.replace(',', ''), end='')


    def main(self):
        self.handle_args()

        args = self.parser.parse_args()

        if (args.download):
            # Activate downloader.py
            print(args)
            raise NotImplementedError
        elif (args.list):
            # Show all systems
            self.showlist()

        elif (args.scrapedatabase):
            # Activate tablescraper.py
            raise NotImplementedError

        elif (args.both):
            # Do both
            raise NotImplementedError

        # Avoid starting a nonexistent handler
        else:
            argparse.print_help()
            sys.exit(2)


if __name__ == "__main__":
    x = ArgHandler()
    x.main()
