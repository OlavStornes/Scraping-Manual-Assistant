import requests
import time
import os
from termcolor import colored, cprint
from datetime import datetime



START_URL = 'http://www.gamesdatabase.org/Media/SYSTEM/{0}//Manual/formated/'
# Nintendo_SNES ---original name with underscore
EXTENSION = '.pdf'



''' Whished format:
http://www.gamesdatabase.org/Media/SYSTEM/
Nintendo_SNES//Manual/formated/
Zombies_Ate_My_Neighbors_-_1993_-_Konami.pdf'''


class Manualdownloader():
    def __init__(self, entry, database, model):
        self.db = database
        self.m_game = model
        self.d_count = 0
        self.e_count = 0
        self.s_count = 0
        self.system = entry.name
        self.system_id = entry.sys_id

        self.prepare_url()

        self.prepare_destination()

    def prepare_destination(self):
        self.newpath = 'data/{}/'.format(self.system)
        if not os.path.exists(self.newpath):
            os.makedirs(self.newpath)

    def prepare_url(self):
        self.system_url = self.sanitize_system_url(self.system)
        self.start_url = START_URL.format(self.system_url)

    def filealreadyexists(self, filepath):
        return os.path.isfile(filepath)

    def sanitize_system_url(self, name):
        for c in r"\":\&/ ":
            name = name.replace(c, '_')
        return name

    def sanitize_request_url(self, name):
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
        game_url = self.sanitize_request_url(game)

        if publisher == 'None':
            publisher_input = ''
        else:
            publisher_input = '_-_' + self.sanitize_request_url(publisher)

        if year == 0:
            year_input = ''
        else:
            year_input = '_-_' + str(year)

        name_postfix = year_input + publisher_input + EXTENSION

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

            cprint("{} - Done => {}  ".format(
                datetime.now().isoformat(' ', 'seconds'),
                self.filepath), 'green')
            time.sleep(2)
            return 'COMPLETED'

        else:
            errorstring = "{} - Error => \n Filepath: {}\n URL: {}".format(
                datetime.now().isoformat(' ', 'seconds'),
                game_obj["name"],
                game_obj['url']
                )
            cprint(errorstring, 'red')
            with open('error.log', 'a') as f:
                f.write(errorstring + '\n')
            return 'ERROR'

    def cleanup(self):

        print("Finished!")
        print("Downloaded: " + str(self.d_count))
        print("Errors: " + str(self.e_count))
        print("Skipped: " + str(self.s_count))

    def main(self):

        status = ''

        query = (self.m_game.select().where(
            self.m_game.system_id == self.system_id))

        # for row in self.models['Game'].
        for row in query:
            game = row.game
            year = row.year
            publisher = row.publisher
            game_obj = self.parse_request_url(game, publisher, year)
            self.filepath = self.newpath + game_obj['name']

            if (self.filealreadyexists(self.filepath)):
                cprint("{} - Skip => {}".format(
                    datetime.now().isoformat(' ', 'seconds'),
                    self.filepath)
                    , 'cyan')
                status = 'SKIPPED'

                self.s_count += 1

                time.sleep(0.05)

            else:
                status = self.send_request(game_obj)
                time.sleep(3)
                if status == 'ERROR':
                    self.e_count += 1
                elif status == 'DOWNLOADED':
                    self.d_count += 1
