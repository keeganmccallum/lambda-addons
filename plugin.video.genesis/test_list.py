import sys
from xbmcadapter import *

sys.modules['xbmc'] = xbmc
sys.modules['xbmcaddon'] = xbmcaddon
sys.modules['xbmcplugin'] = xbmcplugin
sys.modules['xbmcgui'] = xbmcgui
sys.modules['xbmcvfs'] = xbmcvfs

from modules.v4 import shows
from modules.v4 import movies
from modules.v4 import seasons
from modules.v4 import episodes
from modules.sources import sources

import simplejson as json
import datetime


def search(data):
    return {"shows": shows().search(data), "movies": movies().search(data)}


def getSeasons(show):
    return seasons().get(show['title'], show['year'], show['imdb'], show['tvdb'])


def getEpisodes(season):
    return episodes().get(season['show'], season['year'], season['imdb'],
                          season['tvdb'], season['season'])


def getSources(video):
    if video.get('tvdb', '0') == '0':
        # movie
        arguments = ['name', 'title', 'year', 'imdb', None, None, None,
                     None, None, None, None]
    else:
        # tv
        arguments = ['name', 'title', 'year', 'imdb', 'tvdb', 'season', 'episode',
                     'show', 'show_alt', 'date', 'genre']
    args = [
        video.get(arg, None) if arg is not None else None
        for arg in arguments
    ]
    return sources().getSources(*args)


def resolveSource(source):
    src = sources().sourcesResolve(source['url'],
                                   source['provider']).split('|')[0]
    return src

for line in sys.stdin:
    # wait for input from node
    payload = json.loads(line)
    if payload['action'] == 'search':
        val = search(payload['data'])
    elif payload['action'] == 'seasons':
        val = {"seasons": getSeasons(payload['data'])}
    elif payload['action'] == 'episodes':
        val = {"episodes": getEpisodes(payload['data'])}
    elif payload['action'] == 'sources':
        val = {"sources": getSources(payload['data'])}
    elif payload['action'] == 'play':
        val = {"source": resolveSource(payload['data'])}
    else:
        continue
    print json.dumps(val)
