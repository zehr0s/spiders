#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 08:58:00 PM
# Description:  Manga downloader

from lib import Crawler

'''
url = 'https://www.readm.org/manga/16103'
skeleton = {
    'tag': 'h6',
    'filter': {'class' : 'truncate'},
    'tag-target': 'a',
    'filter-target': {}
}
'''

url = 'https://www.readm.org/manga/16103/1/all-pages'
skeleton = {
    'tag': 'img',
    'filter': {'class' : 'img-responsive'},
    'tag-target': None,
    'filter-target': None
}


craw = Crawler(url, skeleton, source='src')
urls = craw.search()
for u in urls:
    print('{}{}'.format('https://www.readm.org',u))
