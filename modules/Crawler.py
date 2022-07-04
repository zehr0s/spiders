#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 07:00:47 PM
# Description:  Class to crawl the web

import requests
from bs4 import BeautifulSoup

''' Filter template
{
    'tag': 'name',                                  # Required: Tag name
    'filter': {'property':'property-name'},         # Required: Tag filter by property (can be empty {})
    'tag-target': 'name',                           # Optional: Tag name (inside previous tag)
    'filter-target': {'property':'property-name'},  # Optional: Tag filter by property (inside previous tag, can be empty {})
    'source': 'source-name'                         # Optional: Tag source, default is 'href' for <a> tags
}
'''

class Crawler:
    ''' Constructor '''
    def __init__(self, source='href', base_url=None, timeout=15):
        self.base_url = base_url
        self.filter = filter
        self.source = source
        self.timeout = timeout
        self.pages = []

    ''' Methods '''
    def search(self, url, filter, use_base_prefix=False):
        # Define tag source
        try:
            source = filter['source']
        except KeyError:
            source = 'href'

        # Request url content
        r = requests.get(url, timeout=self.timeout)
        bs = BeautifulSoup(r.text, 'html.parser')
        self.pages = []

        # Filter tag by filter
        for filtered in bs.find_all(filter['tag'], filter['filter']):
            # Intent to apply second filter inside filtered tags
            try:
                # Second filter
                for out in filtered.find_all(filter['tag-target'], filter['filter-target']):
                    self.pages.append(out[source])
            except KeyError:
                # No second filter required
                self.pages.append(filtered[source])

        self.pages = ['{}{}'.format(self.base_url, page) for page in self.pages] if use_base_prefix else self.pages
        return self.pages

    def reverse_pages(self):
        self.pages.reverse()

    def navigate_pages(self):
        pass
