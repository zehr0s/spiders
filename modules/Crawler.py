#! /usr/bin/env python3

# Author:       Author
# Date:         June 26 2022 at 07:00:47 PM
# Description:  Class to crawl the web

import os
import requests
from bs4 import BeautifulSoup

''' Filter template
{
    'tag': 'name',                                    # Required: Tag name
    'filter': {'attribute':'attribute-name'},         # Required: Tag attribute (can be empty {})
    'tag-target': 'name',                             # Optional: Tag name (inside previous tag)
    'filter-target': {'attribute':'attribute-name'},  # Optional: Tag attribute (inside previous tag, can be empty {})
    'source': 'source-name'                           # Optional: Tag source, default is 'href'
}
'''

class Crawler:
    ''' Constructor '''
    def __init__(self, base_url=None, timeout=15):
        self.base_url = base_url    # Website index
        self.timeout = timeout      # Request timeout
        self.content = None         # Beautiful soup object
        self.pages = []             # Resulting list from search/navigate method
        self.results = []           # Resulting list from search_content/navigate method

    ''' Methods '''
    def __get_number(self, message, error_message='Number must be positive, try again.'):
        while True:
            try:
                number = int(input(message))
                if number > 0:
                    break
                else:
                    print(error_message)
            except ValueError:
                print(error_message)
        return number

    def __request(self, url):
        # Request url content
        r = requests.get(url, timeout=self.timeout)
        self.content = BeautifulSoup(r.text, 'html.parser')
        return self.content

    def search_content(self, filter, use_base_prefix=False):
        # Define tag source
        try:
            source = filter['source']
        except KeyError:
            source = 'href'

        self.results = []
        # Filter tag by filter
        for filtered in self.content.find_all(filter['tag'], filter['filter']):
            # Intent to apply second filter inside filtered tags
            try:
                # Second filter
                for out in filtered.find_all(filter['tag-target'], filter['filter-target']):
                    self.results.append(out[source])
            except KeyError:
                # No second filter required
                self.results.append(filtered[source])

        self.results = ['{}{}'.format(self.base_url, page) for page in self.results] if use_base_prefix else self.results
        return self.results

    def search(self, url, filter, use_base_prefix=False):
        self.__request(url)
        self.pages = self.search_content(filter, use_base_prefix)
        return self.pages

    def reverse_pages(self):
        self.pages.reverse()

    def navigate(self, max=10, items=None):
        items = items if items else self.pages
        total_pages = len(items)
        if (total_pages/max)%1 == 0:
            total_pages = round(total_pages/max)
        else:
            total_pages = round(total_pages/max - (total_pages/max)%1)+1
        flat_list = items
        items = [ items[(i+1)*max-max:(i+1)*max] for i in range(total_pages) ]
        i = 0
        navigating = True

        while navigating:
            item_list = items[i]
            print('\n== Page: {}/{} ==\n'.format(i+1, total_pages))
            for k, name in enumerate(item_list):
                print('{}:\t{}'.format(max*i + k+1, name))
            print('\n[X] Exit\t[N] Next\t[P] Previous\t[S] Select\t', end='')
            option = input('Option: ')
            if option in ['x', 'X']:
                output = flat_list
                break
            elif option in ['n', 'N']:
                i = 0 if i+1 == total_pages else i+1
            elif option in ['p', 'P']:
                i = total_pages-1 if i-1 < 0 else i-1
            elif option in ['s', 'S']:
                print('[X] Back\t[S] Single\t[R] Range\t[A] All\t', end='')
                selection = input('Option: ')
                if selection in ['x', 'X']:
                    pass
                elif selection in ['s', 'S']:
                    while True:
                        index = self.__get_number('Index: ')
                        try:
                            output = [flat_list[index-1]]
                            break
                        except IndexError:
                            print('Invalid index')
                    break
                elif selection in ['r', 'R']:
                    while True:
                        index_a = self.__get_number('Index A: ')
                        index_b = self.__get_number('Index B: ')
                        output = flat_list[index_a-1:index_b]
                        if output:
                            break
                        else:
                            print('Empty list try again')
                    break
                elif selection in ['a', 'A']:
                    output = flat_list
                    break
                else:
                    print('** {} is not an option **'.format(selection))
            else:
                print('** {} is not an option **'.format(option))

        self.results = output
        self.pages = output
        return output

    def save(self, filename='output.log', path='.', custom_list=None, write_type='w'):
        if custom_list == None:
            custom_list = self.pages
        if path != '.':
            os.makedirs(path, exist_ok=True)
        with open('{}/{}'.format(path, filename), write_type) as f:
            for line in custom_list:
                f.write('{}\n'.format(line))
