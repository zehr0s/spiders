#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 08:58:00 PM
# Description:  Manga downloader

from lib import Crawler

base = 'https://www.readm.org'

url = 'https://www.readm.org/manga/16103'
skeleton = {
    'tag': 'h6',
    'filter': {'class' : 'truncate'},
    'tag-target': 'a',
    'filter-target': {}
}

craw = Crawler(url, skeleton)
urls = craw.search()
urls = [ '{}{}'.format(base, url) for url in urls ]

skeleton = {
    'tag': 'img',
    'filter': {'class' : 'img-responsive'},
    'tag-target': None,
    'filter-target': None
}

chapters = []

total = len(chapters)
for i, chapter in enumerate(urls):
    if i == 2:
        break
    print('Chapters: {}/{}'.format(i+1, total))
    craw = Crawler(chapter, skeleton, source='src')
    chapters.append( craw.search() )

for chapter in chapters:
    for page in chapter:
        print('{}{}'.format(base, page))
