#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 08:58:00 PM
# Description:  Manga downloader

from modules import Crawler
from modules import Downloader
from modules.Tools import scrollable
from modules.Tools import grid
import os

# Target
base = 'https://www.readm.org'
# url = 'https://www.readm.org/manga/one-piece' # One Piece
url = 'https://www.readm.org/manga/16103'       # One Punch
# url = 'https://www.readm.org/manga/8064'      # Windbreaker
current_title = 'one-punch-man'
# Filters
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

# Get pages
craw = Crawler(base_url=base)
craw.search(url, link_filter, use_base_prefix=True)
craw.reverse_pages()
craw.navigate()
# craw.save('pages.log', 'logs')

# Get images by chapter
total = len(craw.pages)
chapters = []
titles = []
for i, chapter in enumerate(craw.pages):
    print('Reading chapters: {}/{}'.format(i+1, total))
    titles.append(chapter)
    chapters.append( craw.search(chapter, image_filter, use_base_prefix=True) )
os.system('clear')

# Download images by chapter
dl = Downloader(prefix = 'Pages')
for i, info in enumerate(zip(titles, chapters)):
    title, chapter = info
    print('Chapters: {}/{} - {:.2f}%'.format( i+1, len(chapters), i/len(chapters) ))
    dl.download(chapter, 'manga/one-punch/{}'.format(title.split('/')[-2]))
    os.system('clear')

# Create scroll gallery
scrollable('manga/{}'.format(current_title))
