#! /usr/bin/env python3

from modules import Crawler
from modules import Downloader
from modules.Tools import scrollable
from modules.Tools import grid
import os

# Target
url = 'https://webfapfap.com/celebrity-picture/voezacos-nude-onlyfans-leaks/'
destiny = 'tmp-pictures/webfp'
current_title = 'voeza'

os.makedirs(destiny, exist_ok=True)

# Filters
link_filter = {
    'tag': 'div',
    'filter': {'class' : 'entry-inner'},
    'tag': 'img',
    'filter': {'title': 'Voezacos Nude OnlyFans Leaks'},
    'source': 'src'
}


# Get images
craw = Crawler()
craw.search(url, link_filter)
craw.navigate()

# Download images by chapter
dl = Downloader(prefix = 'Images')
dl.download(craw.pages, '{}/{}'.format(destiny, current_title))


# Create scroll gallery
scrollable('{}'.format(destiny))
grid('{}'.format(destiny))
