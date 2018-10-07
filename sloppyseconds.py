import requests
from bs4 import BeautifulSoup
from termcolor import colored, cprint


def find_href(td_elems):
    cprint("Looking for Game manual button.. ", end='', color='yellow')
    for elem in td_elems:
        if 'Game Manual' in elem.text:
            cprint("Got it!", end='', color='yellow')            
            link = elem.nextSibling.contents[0].attrs['href']
            return link

def href_create_game_obj(href, url):
    if href:
        name = href.split('/')[-1]
    else:
        name = href

    return {
        'name': name,
        'url': url
    }

def sanitize_to_find_href(name):
    name = name.replace('&', 'and')
    
    for c in r"'+\\/:":
        name = name.replace(c, '')

    name = name.replace('  ', ' ')
    
    # Remove leading and trailing whitespaces
    name = name.strip()

    for c in r" ":
        name = name.replace(c, '-')


    return name

def href_find_link_by_name(system, game):    
    BASE = 'http://www.gamesdatabase.org/game/{}/{}'
    MANUAL_BASE = 'http://www.gamesdatabase.org{}'

    system = sanitize_to_find_href(system)
    game = sanitize_to_find_href(game)

    cprint("Game: {} ".format(game), end='', color='yellow')
    url = BASE.format(system, game)
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    try:
        table_elems = soup.find_all('table')[5]
    except IndexError as i:
        return False

    td_elems = table_elems.find_all('td')


    href = find_href(td_elems)
    if href:
        proper_url = MANUAL_BASE.format(href)
        cprint(proper_url, 'yellow') 

        game_obj = href_create_game_obj(href, proper_url)
        return game_obj
    else:
        notfound_obj = href_create_game_obj(False, 'Not found')
        cprint('Button not found', 'yellow')
        return notfound_obj