#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 08:58:00 PM
# Description:  Manga downloader

from lib import Crawler

base = 'https://www.readm.org'
url = 'https://www.readm.org/manga/16103'

link_filter = {
    'tag': 'h6',
    'filter': {'class' : 'truncate'},
    'tag-target': 'a',
    'filter-target': {}
}

image_filter = {
    'tag': 'img',
    'filter': {'class' : 'img-responsive'},
    'source': 'src'
}

craw = Crawler(base_url=base)
craw.search(url, link_filter, use_base_prefix=True)
craw.reverse_pages()
total = len(craw.pages)

chapters = []
for i, chapter in enumerate(craw.pages):
    if i == 2:
        break
    print('Chapters: {}/{}'.format(i+1, total))
    chapters.append( craw.search(chapter, image_filter, use_base_prefix=True) )

for chapter in chapters:
    for page in chapter:
        print(page)
