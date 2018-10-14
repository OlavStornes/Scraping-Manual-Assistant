import requests
import time
import os
import glob
from termcolor import cprint
from datetime import datetime
import sloppyseconds as ss


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

    def filealreadyexists(self, filepath, basename):
        x = os.path.isfile(filepath)
        if x:
            return True
        else:
            sane_name = self.sanitize_filename(basename)
            y = glob.glob(self.newpath + sane_name + "*")
            if y:
                self.filepath = y[0]
                return True

        return False

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
        tmp = {"name": filename, "url": request_url, 'originaltitle': game}
        return tmp

    def send_request(self, url):
        x = requests.get(url, stream=True)
        return x

    def write_manual(self, response, path):
        cprint("{} -".format(datetime.now().isoformat(' ', 'seconds')),
               end='', color='green')
        with open(path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024):
                fd.write(chunk)

        cprint(" Done => {}  ".format(path), 'green')
        self.d_count += 1
        time.sleep(2)

    def workaround_attempt(self, game):
        newurl_obj = ss.href_find_link_by_name(self.system, game)
        if newurl_obj['name']:
            newurl_obj['name'] = self.newpath + \
                newurl_obj['name'].replace('_', ' ')
            response = self.send_request(newurl_obj['url'])
            self.filepath = newurl_obj['name']

            return response, newurl_obj
        else:
            return None, newurl_obj['url']

    def attempt_download(self, game_obj):
        response = self.send_request(game_obj['url'])

        if response.ok:
            self.write_manual(response, self.filepath)

        else:
            # Attempt to go through manually first. Slower, but accurate
            cprint("First attempt failed, trying a workaround...", 'yellow')
            response, attempted_url = self.workaround_attempt(
                game_obj['originaltitle'])
            if response:
                self.write_manual(response, self.filepath)
            else:
                self.e_count += 1
                errorstring = "{} - Error => \n Filepath: {}\n 1st URL: {} \n 2nd URL: {}".format(
                    datetime.now().isoformat(' ', 'seconds'),
                    game_obj["name"],
                    game_obj['url'],
                    attempted_url
                )
                cprint(errorstring, 'red')

                with open('error.log', 'a') as f:
                    f.write(errorstring + '\n')

    def cleanup(self):

        print("Finished downloading for {}!".format(self.system))

    def get_report(self):
        return {
            'System': self.system,
            'Downloaded': self.d_count,
            'Errors': self.e_count,
            'Skipped': self.s_count
        }

    def main(self):
        query = (self.m_game.select().where(
            self.m_game.system_id == self.system_id))

        total_queries = len(query)

        # for row in self.models['Game'].
        for index, row in enumerate(query):
            print(f'{index}/{total_queries} ', end='')
            game = row.game
            year = row.year
            publisher = row.publisher
            game_obj = self.parse_request_url(game, publisher, year)
            self.filepath = self.newpath + game_obj['name']

            if (self.filealreadyexists(self.filepath, game)):
                cprint("{} - Skip => {}".format(
                    datetime.now().isoformat(' ', 'seconds'),
                    self.filepath), 'cyan')

                self.s_count += 1

                time.sleep(0.05)

            else:
                self.attempt_download(game_obj)
                time.sleep(3)

        self.cleanup()
