#! /usr/bin/env bash

# Author:       Author
# Date:         June 26 2022 at 07:00:47 PM
# Description:  Class to crawl the web

import requests
from bs4 import BeautifulSoup

class Crawler:
    ''' Body template
    {
        'tag': 'name',
        'filter': {'property':'property-name'},
        'tag-target': 'name',
        'filter-target': {'property':'property-name'}
    }
    '''
    def __init__(self, url, body, source='href', timeout=15):
        self.url = url
        self.body = body
        self.source = source
        self.timeout = timeout
    def search(self):
        r = requests.get(self.url, timeout=self.timeout)
        bs = BeautifulSoup(r.text, 'html.parser')
        # print( bs.prettify() )
        output = []
        # TODO: Maybe generalize this part
        for filtered in bs.find_all(self.body['tag'], self.body['filter']):
            if self.body['tag-target'] is None:
                output.append(filtered[self.source])
            else:
                for out in filtered.find_all(self.body['tag-target'], self.body['filter-target']):
                    output.append(out[self.source])
        return output

    # TODO: Crawl throgh pages
