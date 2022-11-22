#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 08:58:00 PM
# Description:  Manga downloader

from modules import Crawler
from modules import Downloader
from modules.Tools import create_gallery
import os

# Target
base = 'https://luminousscans.com'
search = base + '/?s=wind+breaker'
current_title = 'windbreaker'

# Filters
link_filter = {
    'tag': 'div',
    'filter': {'class' : 'listupd'},
    'tag-target': 'a',
    'filter-target': {},
    'source': 'href'
}

# Get series' url
craw = Crawler(base_url=base)
craw.search(search, link_filter, use_base_prefix=False)
url = craw.pages[0]

# Filters
link_filter = {
    'tag': 'div',
    'filter': {'class' : 'chbox'},
    'tag-target': 'a',
    'filter-target': {},
    'source': 'href'
}

image_filter = {
    'tag': 'img',
    'filter': {'class' : 'size-full'},
    'source': 'src'
}

# Get pages
craw.search(url, link_filter, use_base_prefix=False)
# craw.reverse_pages()
craw.navigate()
# craw.save('pages.log', 'logs')

# Get images by chapter
total = len(craw.pages)
chapters = []
titles = []
for i, chapter in enumerate(craw.pages):
    print('Reading chapters: {}/{}'.format(i+1, total))
    titles.append(chapter)
    chapters.append( craw.search(chapter, image_filter, use_base_prefix=False) )
os.system('clear')

# Download images by chapter
dl = Downloader(prefix = 'Pages')
for i, info in enumerate(zip(titles, chapters)):
    title, chapter = info
    if len(chapter) == 0:
        continue
    print('Chapters: {}/{} - {:.2f} %'.format( i+1, len(chapters), i/len(chapters)*100 ))
    dl.download(chapter, 'manga/{}/{}'.format(current_title, title.split('/')[-2].split('-')[-1]))
    os.system('clear')

# Create scrollable gallery
create_gallery('manga/{}'.format(current_title), type='scrollable')


# TODO: Create gallery and update menu
# create_menu('manga/{}'.format(current_title), type='scrollable')
