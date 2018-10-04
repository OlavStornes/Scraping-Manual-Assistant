import requests
import openpyxl
import time
import os
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
import re

START_URL = 'http://www.gamesdatabase.org/Media/SYSTEM/Nintendo_SNES//Manual/formated/'
EXTENSION = '.pdf'

COL_GAME = 'B'
COL_PUB = 'F'
COL_YEAR = 'J'
COL_STATUS = 'K'


''' Whished format:
http://www.gamesdatabase.org/Media/SYSTEM/
Nintendo_SNES//Manual/formated/
Zombies_Ate_My_Neighbors_-_1993_-_Konami.pdf'''


def sheet_writestatus(sheet, rowstr):
    cell = sheet[COL_STATUS+rowstr] 
    cell.font = Font(color=colors.BLUE)
    cell.value = "X"


def save_database(wb):
    try:
        wb.save('Gamelist.xlsx')
    except:
        print ("error writing to database")


def filealreadyexists(game_obj):
    return os.path.isfile(game_obj['name'])


def sanitize_gamename(name):
    for c in r"'?\":\&*/":
        name = name.replace(c, '-')

    for d in r" ":
        name = name.replace(d, '_')

    return name

def sanitize_filename(name):
    #Attemtpting to abide by windows' file standard
    for c in r'/\\?\;:>"<*^|':
        name = name.replace(c,'')
    return name

def parse_request_url(game, publisher, year):
    game_url = sanitize_gamename(game)
    publisher = publisher.replace(' ', '_').replace('&', '-')

    name_postfix = '_-_' + str(year) + '_-_' + publisher + EXTENSION

    filename = game + name_postfix.replace('_', ' ')
    filename = sanitize_filename(filename)

    
    request_url = START_URL + game_url + name_postfix
    tmp = {"name": filename, "url": request_url}
    return tmp

def send_request(game_obj):
    response = requests.get(game_obj['url'], stream=True)


    if response.ok:
        with open(game_obj['name'], 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024):
                fd.write(chunk)

        print("Downloaded " + game_obj['name'])
        time.sleep(5)
        return 'COMPLETED'

    else:
        errorstring = "Error downloading " + game_obj["name"] +  " at " + game_obj['url']
        print(errorstring)
        with open('error.log', 'a') as f:
            f.write(errorstring + '\n')
        return 'ERROR'

def main():
    d_count = 0
    e_count = 0
    s_count = 0

    wb = openpyxl.load_workbook('Gamelist.xlsx')
    sheet_snes = wb['SNES']
    status = ''


    for row in range(2, sheet_snes.max_row):
        rowstr = str(row)
        game =      sheet_snes[COL_GAME+rowstr].value
        publisher = sheet_snes[COL_PUB+rowstr].value
        year =      sheet_snes[COL_YEAR+rowstr].value
        game_obj = parse_request_url(game, publisher, year)

        if (filealreadyexists(game_obj)):
            print("%s already exists - skipping" %(game_obj['name']))
            status = 'SKIPPED'
            sheet_writestatus(sheet_snes, rowstr)

            s_count += 1
            
            time.sleep(0.05)

        else:
            status = send_request(game_obj)
            time.sleep(3)
            if status == 'ERROR':
                e_count += 1
            elif status == 'DOWNLOADED':
                sheet_writestatus(sheet_snes, rowstr)
                d_count += 1

        if row % 50 == 0:
            save_database(wb)


#########################################################

    save_database(wb)

    print("Finished!")
    print("Downloaded: " + str(d_count))
    print("Errors: " + str(e_count))
    print("Skipped: " + str(s_count))

if (__name__ == "__main__"):
    main()
