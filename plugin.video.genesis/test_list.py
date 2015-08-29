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

    src = sources()
    src.sources = src.getSources(*args)
    return src.sourcesFilter()


def resolveSource(source):
    src = sources().sourcesResolve(source['url'],
                                   source['provider']).split('|')[0]
    return src

# show = search("power")["shows"][0]
# season = getSeasons(show)[0]
# episode = getEpisodes(season)[3]
# print json.dumps(getSources({ 'rating': '8.0',
#   'show': 'Power',
#   'genre': 'Drama',
#   'imdb': '3281796',
#   'year': '2014',
#   'duration': '60',
#   'plot': 'A model gets hospitalized after snorting bad cocaine. Ghost, Tommy and Josh investigate, while Josh suggests to involve police. The rift between Tasha and Ghost deepens when she visits the bank to find a lot of their money missing.',
#   'thumb': 'http://thetvdb.com/banners/episodes/276562/4851168.jpg',
#   'title': 'This Is Real',
#   'tvdb': '276562',
#   'mpaa': 'TV-MA',
#   'writer': 'Lauren Schmidt',
#   'season': '1',
#   'status': 'Continuing',
#   'poster': 'http://thetvdb.com/banners/posters/276562-5.jpg',
#   'director': 'John David Coles',
#   'studio': 'Starz!',
#   'date': '2014-06-21',
#   'banner': 'http://thetvdb.com/banners/graphical/276562-g8.jpg',
#   'episode': '3',
#   'name': 'Power S01E03',
#   'url': 'http://www.imdb.com/title/tt3281796/',
#   'fanart': 'http://thetvdb.com/banners/fanart/original/276562-13.jpg',
#   'show_alt': 'Power' }
# ))

for line in sys.stdin:
    # try:
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
    # except:
    #     print "{}"
    #     break
