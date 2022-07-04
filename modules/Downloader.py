#! /usr/bin/env python3

# Author:       Author
# Date:         July 04 2022 at 04:27:36 PM
# Description:  Download images from a list or .log file

# Modules
import requests
import shutil
import sys
import os

class Downloader:
    # Class attributes
    def __init__(self, prefix='Downloading', timeout=15):
        self.timeout = timeout
        self.prefix = prefix

    def print_custom(self, message, type=0):
        '''
        type
            0: status
            1: error
            2: success
        '''
        # os.system('clear')
        if type == 0:               # status
            print('[+] {}: {}'.format(self.prefix, message))
        elif type == 1:             # error
            print('[!] {}: {}'.format(self.prefix, message))
        else:                       # success
            print('[*] {}: {}'.format(self.prefix, message))

    def download(self, links, download_path='output_files'):
        os.makedirs(download_path, exist_ok=True)
        # Iterate pages
        for i, img_url in enumerate(links):
            # Request image
            try:
                r = requests.get(img_url, timeout=self.timeout)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                self.print_custom('Timeout in page url {}'.format(img_url), type=1)
                # Remove incomplete download
                shutil.rmtree('{}'.format(download_path))
                sys.exit(1)
            except KeyboardInterrupt:
                self.print_custom('Keyboad Interrupt in {}'.format(img_url), type=1)
                # Remove incomplete download
                shutil.rmtree('{}'.format(download_path))
                sys.exit(1)
            except:
                self.print_custom('Error in {}'.format(img_url), type=1)
                # Remove incomplete download
                shutil.rmtree('{}'.format(download_path))
                sys.exit(1)
            if not r.ok:
                self.print_custom('Connection error in page url {}'.format(img_url), type=1)
                # remove incomplete download
                shutil.rmtree('{}'.format(download_path))
                sys.exit(1)

            # download page
            with open('{}/{:02}.jpg'.format(download_path, i+1), 'wb') as f:
                f.write(r.content)

            # update status
            total = len(links)
            self.print_custom('{:.2f}%'.format( (i+1)/total*100 ))

