import sys
from xbmcadapter import *

sys.modules['xbmc'] = xbmc
sys.modules['xbmcaddon'] = xbmcaddon
sys.modules['xbmcplugin'] = xbmcplugin
sys.modules['xbmcgui'] = xbmcgui
sys.modules['xbmcvfs'] = xbmcvfs

from modules.v4 import shows
from modules.v4 import seasons
from modules.v4 import episodes
from modules.sources import sources


def getUserSelection(options, attr):
    for i, o in enumerate(options):
        print str(i+1) + ". " + str(o[attr])
    return options[input("Enter a selection number: ")-1]


def getShow(options):
    print "Choose Show: "
    return getUserSelection(options, 'title')


def getSeason(options):
    print "Select Season: "
    return getUserSelection(options, 'season')


def getEpisode(options):
    print "Select Episode: "
    return getUserSelection(options, 'episode')


def getQuery():
    return raw_input("Enter TV Show to search for: ")

_shows = shows().search(getQuery())
show = getShow(_shows)

_seasons = seasons().get(show['title'], show['year'], show['imdb'], show['tvdb'])
season = getSeason(_seasons)

_episodes = episodes().get(season['show'], season['year'], season['imdb'],
                           season['tvdb'], season['season'])
episode = getEpisode(_episodes)

args = [
    episode[arg]
    for arg in 'name', 'title', 'year', 'imdb', 'tvdb', 'season', 'episode',
               'show', 'show_alt', 'date', 'genre'
]

PAGE_SIZE = input("Page Size: ")

_sources = map(lambda s: s.split('|')[0],
               filter(lambda src: src is not None,
                      [sources().sourcesResolve(i['url'], i['provider'])
                       for i in sources().getSources(*args)[:PAGE_SIZE]]
                      )
               )

print "Sources: "
for i, s in enumerate(_sources):
    print str(i+1) + ". " + s
