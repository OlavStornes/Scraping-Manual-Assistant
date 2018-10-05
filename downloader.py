import requests
import openpyxl
import time
import os
from openpyxl.styles import colors
from openpyxl.styles import Font

START_URL = 'http://www.gamesdatabase.org/Media/SYSTEM/{0}//Manual/formated/'
# Nintendo_SNES ---original name with underscore
EXTENSION = '.pdf'

COL_GAME = 'A'
COL_PUB = 'C'
COL_YEAR = 'F'
COL_STATUS = 'G'


''' Whished format:
http://www.gamesdatabase.org/Media/SYSTEM/
Nintendo_SNES//Manual/formated/
Zombies_Ate_My_Neighbors_-_1993_-_Konami.pdf'''


class Manualdownloader():
    def __init__(self, target_system):
        self.d_count = 0
        self.e_count = 0
        self.s_count = 0
        self.system = target_system

        self.prepare_url()

        self.prepare_destination()

    def prepare_destination(self):
        self.newpath = 'data/{}/'.format(self.system)
        if not os.path.exists(self.newpath):
            os.makedirs(self.newpath)

    def prepare_url(self):
        self.system_url = self.sanitize_system_url(self.system)

        self.start_url = START_URL.format(self.system_url)
        
    def sheet_writestatus(self, rowstr):
        cell = self.sheet[COL_STATUS+rowstr]
        cell.font = Font(color=colors.BLUE)
        cell.value = "X"

    def save_database(self):
        try:
            self.wb.save('Gamelist.xlsx')
        except PermissionError:
            print("Error writing to database")

    def filealreadyexists(self, filepath):
        return os.path.isfile(filepath)

    def sanitize_system_url(self, name):
        for c in r"\":\&/ ":
            name = name.replace(c, '_')
        return name

    def sanitize_gamename(self, name):
        for c in r"'?\":\&*/":
            name = name.replace(c, '-')

        for d in r" ":
            name = name.replace(d, '_')

        return name

    def sanitize_filename(self, name):
        # Attemtpting to abide by windows' file standard
        for c in r'/\\?\;:>"<*^|':
            name = name.replace(c, '')
        return name

    def parse_request_url(self, game, publisher, year):
        game_url = self.sanitize_gamename(game)
        publisher = publisher.replace(' ', '_').replace('&', '-')

        name_postfix = '_-_' + str(year) + '_-_' + publisher + EXTENSION

        filename = game + name_postfix.replace('_', ' ')
        filename = self.sanitize_filename(filename)

        request_url = self.start_url + game_url + name_postfix
        tmp = {"name": filename, "url": request_url}
        return tmp

    def send_request(self, game_obj):
        response = requests.get(game_obj['url'], stream=True)

        if response.ok:
            with open(self.filepath, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)

            print("Downloaded " + game_obj['name'])
            time.sleep(5)
            return 'COMPLETED'

        else:
            errorstring = "Error downloading " + \
                game_obj["name"] + " at " + game_obj['url']
            print(errorstring)
            with open('error.log', 'a') as f:
                f.write(errorstring + '\n')
            return 'ERROR'

    def cleanup(self):
        self.save_database()

        print("Finished!")
        print("Downloaded: " + str(self.d_count))
        print("Errors: " + str(self.e_count))
        print("Skipped: " + str(self.s_count))

    def main(self):

        self.wb = openpyxl.load_workbook('Gamelist.xlsx')
        self.sheet = self.wb[self.system]
        status = ''

        for row in range(2, self.sheet.max_row):
            rowstr = str(row)
            game = self.sheet[COL_GAME+rowstr].value
            year = self.sheet[COL_YEAR+rowstr].value
            publisher = self.sheet[COL_PUB+rowstr].value
            game_obj = self.parse_request_url(game, publisher, year)
            self.filepath = self.newpath + game_obj['name']

            if (self.filealreadyexists(self.filepath)):
                print("%s already exists - skipping" % (game_obj['name']))
                status = 'SKIPPED'
                self.sheet_writestatus(rowstr)

                self.s_count += 1

                time.sleep(0.05)

            else:
                status = self.send_request(game_obj)
                time.sleep(3)
                if status == 'ERROR':
                    self.e_count += 1
                elif status == 'DOWNLOADED':
                    self.sheet_writestatus(rowstr)
                    self.d_count += 1

            if row % 50 == 0:
                self.save_database()


#########################################################


if (__name__ == "__main__"):
    x = Manualdownloader("Atari Lynx")
    x.main()
