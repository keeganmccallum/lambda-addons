# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import json
from modules.libraries import client


def resolve(url):
    try:
        url = url.split('/preview', 1)[0]
        url = url.replace('drive.google.com', 'docs.google.com')

        result = client.request(url)
        result = re.compile('"fmt_stream_map",(".+?")').findall(result)[0]

        u = json.loads(result)
        u = [i.split('|')[-1] for i in u.split(',')]
        u = sum([tag(i) for i in u], [])

        url = []
        try: url += [[i for i in u if i['quality'] == '1080p'][0]]
        except: pass
        try: url += [[i for i in u if i['quality'] == 'HD'][0]]
        except: pass
        try: url += [[i for i in u if i['quality'] == 'SD'][0]]
        except: pass

        if url == []: return
        return url
    except:
        return


def tag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try: quality = quality[0]
    except: return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080p', 'url': url}]
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': 'HD', 'url': url}]
    elif quality in ['35', '44', '135', '244', '94']:
        return [{'quality': 'SD', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': 'SD', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': 'SD', 'url': url}]
    else:
        return []

