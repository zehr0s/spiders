#! /usr/bin/env python3

# Author:       Author
# Date:         July 04 2022 at 04:27:36 PM
# Description:  Download images from a list or .log file

# Modules
import requests
import shutil
import sys
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class Downloader:
    # Class attributes
    def __init__(self, prefix='Downloading', timeout=60):
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


    def download_image(self, info):
        i, img_url, download_path = info
        start_time = datetime.now()
        try:
            r = requests.get(img_url, timeout=self.timeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            self.print_custom('Timeout in page url {}'.format(img_url), type=1)
            shutil.rmtree(download_path, ignore_errors=True)
            return None
        except KeyboardInterrupt:
            self.print_custom('Keyboard Interrupt in {}'.format(img_url), type=1)
            shutil.rmtree(download_path, ignore_errors=True)
            sys.exit(1)
        except Exception as e:
            self.print_custom(f"Error in {img_url}: {str(e)}", type=1)
            shutil.rmtree(download_path, ignore_errors=True)
            return None

        if not r.ok:
            self.print_custom('Connection error in page url {}'.format(img_url), type=1)
            shutil.rmtree(download_path, ignore_errors=True)
            return None

        # Save the image
        image_path = f'{download_path}/{i+1:02}.jpg'
        with open(image_path, 'wb') as f:
            f.write(r.content)

        end_time = datetime.now()
        dt_s = (end_time - start_time).seconds

        # Update status
        return (i, dt_s, len(r.content))


    def download(self, links, workers=4, download_path='output_files'):
        # Use ThreadPoolExecutor to download images in parallel
        with ThreadPoolExecutor(max_workers=workers) as executor:  # Adjust max_workers as needed
            futures = {executor.submit(self.download_image, (i, img_url, download_path)): i for i, img_url in enumerate(links)}

            total = len(links)
            for i, future in enumerate(as_completed(futures)):
                result = future.result()
                if result is not None:
                    idx, dt_s, content_length = result
                    self.print_custom('{:.2f}% | {}s | {} bytes'.format((idx+1)/total*100, dt_s, content_length))
                else:
                    self.print_custom('Failed to download image {}/{}'.format(i+1, total))

#        os.makedirs(download_path, exist_ok=True)
#        # Iterate pages
#        for i, img_url in enumerate(links):
#            start_time = datetime.now()
#            # Request image
#            try:
#                r = requests.get(img_url, timeout=self.timeout)
#            except (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
#                self.print_custom('Timeout in page url {}'.format(img_url), type=1)
#                # Remove incomplete download
#                shutil.rmtree('{}'.format(download_path))
#                continue
#            except KeyboardInterrupt:
#                self.print_custom('Keyboad Interrupt in {}'.format(img_url), type=1)
#                # Remove incomplete download
#                shutil.rmtree('{}'.format(download_path))
#                sys.exit(1)
#            except:
#                self.print_custom('Error in {}'.format(img_url), type=1)
#                # Remove incomplete download
#                shutil.rmtree('{}'.format(download_path))
#                continue
#            if not r.ok:
#                self.print_custom('Connection error in page url {}'.format(img_url), type=1)
#                # remove incomplete download
#                shutil.rmtree('{}'.format(download_path))
#                continue
#
#            # download page
#            with open('{}/{:02}.jpg'.format(download_path, i+1), 'wb') as f:
#                f.write(r.content)
#            end_time = datetime.now()
#            dt_s = (end_time - start_time).seconds
#
#            # update status
#            total = len(links)
#            self.print_custom('{:.2f}% | {}s'.format( (i+1)/total*100, dt_s ))

