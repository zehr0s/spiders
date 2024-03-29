#! /usr/bin/env python3

# Author:       Author
# Date:         July 30 2022 at 08:56:18 AM
# Description:  TikTok Video Downloader

''' Libraries '''
import os
import re
import sys
import time
import json
import random
import string
import requests
import datetime
from bs4 import BeautifulSoup

''' Variables '''

mobile = True
out_path = 'dl_videos'
timeout = 15
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/5311 (KHTML, like Gecko) Chrome/40.0.821.0 Mobile Safari/5311',
}

''' Functions '''
def getChars(lenght, numbers=False):
    if numbers:
        return ''.join(random.choice(string.digits) for i in range(lenght))
    else:
        return ''.join(random.choice(string.ascii_lowercase) for i in range(lenght))

''' Main '''
if len(sys.argv) == 2:
    link = sys.argv[1]
elif len(sys.argv) == 3:
    link = sys.argv[1]
    out_path = sys.argv[2]
else:
    print('{} <url> <output-path>'.format(sys.argv[0]))
    sys.exit(1)

# Get video source
# "canonical": "https://www.tiktok.com/@sluts4plantsandsadmusic/video/7201276881952410886" from  https://vm.tiktok.com/ZMYA9S49L/
r0 = requests.get(link, timeout=timeout, headers=headers)
bs = BeautifulSoup(r0.text, 'html.parser')

# Get video meta data
meta = re.search('{.*AppContext.*}', bs.prettify()).group()
meta = json.loads(meta)
# with open('data.json', 'w') as f:
#     f.write(json.dumps(meta))
video_url  = meta['SEOState']['canonical']

# Get download meta data
try:
    r1 = requests.get(video_url, timeout=timeout, headers=headers)
    bs = BeautifulSoup(r1.text, 'html.parser')
    with open('data.json', 'w') as f:
        f.write(bs.prettify())
    sys.exit()
    meta = json.loads(re.search('{.*downloadAddr.*}', bs.prettify()).group())
    id = list(meta['ItemModule'].keys())[0]
    author = meta['ItemModule'][id]['author']
    v_format = meta['ItemModule'][id]['video']['format']
    v_quality = meta['ItemModule'][id]['video']['videoQuality']
    v_definition = meta['ItemModule'][id]['video']['definition']
    dl_addr = meta['ItemModule'][id]['video']['playAddr']

    # Print info
    if mobile:
        out_name = os.path.join(out_path, '{}-{}-{}-{}.{}'.format(author, id, v_quality, v_definition, v_format.lower()))
    else:
        out_path = os.path.join(out_path, author)
        out_name = os.path.join(out_path, '{}-{}-{}.{}'.format(id, v_quality, v_definition, v_format.lower()))
    print(
        'Downloading {}:\n\tUser: {}\n\tVideo ID: {}\n\tQuality: {}\n\tDefinition: {}\n\tFormat: {}'
        .format(out_name, author, id, v_quality, v_definition, v_format.lower())
    )
except:
    # Print info
    id = video_url.split('/')[-1]
    author = video_url.split('/')[-3][1:]
    if mobile:
        out_name = os.path.join(out_path, '{}-{}-{}.{}'.format(author,id,datetime.date.today(),'mp4'))
    else:
        out_path = os.path.join(out_path, author)
        out_name = os.path.join(out_path, '{}-{}.{}'.format(id,datetime.date.today(),'mp4'))
    print(
        'Downloading {}:\n\tUser: {}\n\tVideo ID: {}'
        .format(out_name, author,id)
    )

# Request video download url

cookies = {
    # '__cflb': '02DiuEcwseaiqqyPC5qqJA27ysjsZzMZ84oUqfS7Ubkqy'
    '__cflb': '__cflb=02DiuEcwseaiqqyPC5qqJA27ysjsZzMZ8SSK3Ed6EULbV'
}

params = {
    'url': 'dl',
}
# r_aux = requests.post('https://ssstik.io/abc')
# cookies = r_aux.cookies.get_dict()

print(f'\tBase URL: {link}')
print(f'\tVideo URL: {video_url}')

for dl_try in range(32):
    time.sleep(2)
    data = {
        'id': video_url,
        'locale': 'en',
        # 'tt': 'blNvVie5',
        'tt': f'{getChars(2)}{getChars(1).upper()}{getChars(1)}{getChars(1).upper()}{getChars(2)}{getChars(1, numbers=True)}'
    }
    r3 = requests.post('https://ssstik.io/abc', headers=headers, params=params, data=data, cookies=cookies)
    if not r3.ok:
        raise Exception(f"Status Code: {r3.status_code}")
    bs = BeautifulSoup(r3.text, "html.parser")
    # print(bs.find_all('a')[0]['href'])
    downloadables = []
    try:
        downloadables = [soup['href'] for soup in bs.find_all('a')]
    except KeyError:
        for downloadable in [soup for soup in bs.find_all('a')]:
            try:
                html_obj = downloadable.get('href')
            except:
                continue
            if html_obj and html_obj.startswith('http'):
                downloadables.append(html_obj)
    except Exception as e:
        raise e
    try:
        downloadables.pop()
        if downloadables:
            break
    except IndexError:
        print(f'\tTry: {dl_try+1}')

total = len(downloadables)
for i, downloadable in enumerate(downloadables[::-1]):
    try:
        r4 = requests.get(downloadable, headers=headers)
    except:
        continue
    if not r4.ok and total == i+1:
        raise Exception(f"Status Code: {r4.status_code}")

# Create output path
os.makedirs(out_path, exist_ok=True)

# Download video
with open(out_name, 'wb') as f:
    for chunk in r4.iter_content(chunk_size = 1024*1024):
        if chunk:
            f.write(chunk)
