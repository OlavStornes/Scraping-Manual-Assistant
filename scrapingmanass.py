import sys
import argparse
import time
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


    def show_results(self, report_list):
        print('\n\nTargeted systems report:')

        total_downloaded = 0
        total_skipped = 0
        total_errors = 0


        for report in report_list:
            print('System: ' + report['System'])
            cprint('\tDownloaded:\t' + str(report['Downloaded']), 'green')
            cprint('\tSkipped:\t' + str(report['Skipped']), 'cyan')
            cprint('\tErrors: \t' + str(report['Errors']), 'red')
            total_downloaded += report['Downloaded']
            total_skipped += report['Skipped']
            total_errors += report['Errors']
            
        if len(report_list) > 1:
            print("\n\n") 
            cprint('Total downloads:\t' + str(total_downloaded), 'green')
            cprint('Total skipped:\t\t' + str(total_skipped), 'cyan')
            cprint('Total errors:\t\t' + str(total_errors), 'red')
            


    def downloadmanual(self, args, skip_confirmation):
        query = data.System.select().where(data.System.sys_id.in_(args))
        report_list = []


        confirm_string = 'Download the database for one or multiple systems'
        self.confirm_action(query, confirm_string, skip_confirmation)

        for entry in query:

            mandownloader = dl.Manualdownloader(
                entry, self.db, self.models['Game'])
            mandownloader.main()
            report_list.append(mandownloader.get_report())
            time.sleep(3)

        # Finished with all downloading
        self.show_results(report_list)


    def scrapedatabase(self, args, skip_confirmation):
        query = data.System.select().where(data.System.sys_id.in_(args))

        confirm_string = 'Scrape game info from the website'
        self.confirm_action(query, confirm_string, skip_confirmation)

        for entry in query:
            scraper = ts.Scrapie(entry, self.db, self.models['Game'])
            scraper.run()
            time.sleep(3)

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
        
    def unpack_ranges(self, args):
        unpacked_args = []
        for argument in args:
            if '-' in argument:
                x = argument.split('-')
                start, stop = int(x[0]), int(x[1])
                unpacked_args.extend(range(start, stop+1))
            else:
                unpacked_args.append(argument)
        return unpacked_args

    def main(self):
        self.handle_args()

        cprint("\nWelcome to the Scraping Manual Assistant!\n", 'green')

        args = self.parser.parse_args()

        skip_confirmation = args.yes

        if (args.list):
            # Show all systems
            self.showlist()
        elif (args.download):
            # Activate downloader.py
            args_input = self.unpack_ranges(args.download)
            self.downloadmanual(args_input, skip_confirmation)

        elif (args.scrapedatabase):
            # Activate tablescraper.py
            args_input = self.unpack_ranges(args.scrapedatabase)
            self.scrapedatabase(args_input, skip_confirmation)

        elif (args.both):
            # Do both
            args_input = self.unpack_ranges(args.both)
            self.scrape_and_download(args_input, skip_confirmation)

        # Avoid starting a nonexistent handler
        else:
            self.parser.print_help()
            sys.exit(2)


if __name__ == "__main__":
    x = ArgHandler()
    x.main()
