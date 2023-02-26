#! /usr/bin/env python3

# Author:       Author
# Date:         July 30 2022 at 08:56:18 AM
# Description:  TikTok Video Downloader

''' Libraries '''
import os
import re
import sys
import json
import requests
from bs4 import BeautifulSoup

''' Variables '''

out_path = 'dl_videos'
timeout = 15
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/5311 (KHTML, like Gecko) Chrome/40.0.821.0 Mobile Safari/5311',
}

''' Main '''
if len(sys.argv) == 2:
    link = sys.argv[1]
elif len(sys.argv) == 3:
    link = sys.argv[1]
    out_path = sys.argv[2]
else:
    print('{} <url> <output-path>'.format(sys.argv[0]))
    sys.exit(1)

print('Requesting data ...')

# Get video source
# "canonical": "https://www.tiktok.com/@sluts4plantsandsadmusic/video/7201276881952410886"
r0 = requests.get(link, timeout=timeout, headers=headers)
bs = BeautifulSoup(r0.text, 'html.parser')

# Get video meta data
meta = re.search('{.*AppContext.*}', bs.prettify()).group()
meta = json.loads(meta)
video_url  = meta['SEO']['canonical']

# Get download meta data
r1 = requests.get(video_url, timeout=timeout, headers=headers)
bs = BeautifulSoup(r1.text, 'html.parser')
meta = json.loads(re.search('{.*downloadAddr.*}', bs.prettify()).group())
id = list(meta['ItemModule'].keys())[0]
author = meta['ItemModule'][id]['author']
v_format = meta['ItemModule'][id]['video']['format']
v_quality = meta['ItemModule'][id]['video']['videoQuality']
v_definition = meta['ItemModule'][id]['video']['definition']
dl_addr = meta['ItemModule'][id]['video']['playAddr']

# Print info
out_path = os.path.join(out_path, author)
out_name = os.path.join(out_path, '{}-{}-{}.{}'.format(id, v_quality, v_definition, v_format.lower()))
print(
    '\nDownloading {}:\n\tUser: {}\n\tVideo ID: {}\n\tQuality: {}\n\tDefinition: {}\n\tFormat: {}'
    .format(out_name, author, id, v_quality, v_definition, v_format.lower())
)


# Request video download url

cookies = {
    '__cflb': '02DiuEcwseaiqqyPC5qqJA27ysjsZzMZ84oUqfS7Ubkqy'
#    '_ga': 'GA1.2.1429312257.1677318021',
#    '_gid': 'GA1.2.378579401.1677318021',
#    '_gat_UA-3524196-6': '1',
}

data = {
    'id': video_url,
    'locale': 'en',
    'tt': 'blNvVUE5',
}

params = {
    'url': 'dl',
}

print(f'\tBase URL: {link}')
print(f'\tVideo URL: {video_url}')

r3 = requests.post('https://ssstik.io/abc', headers=headers, params=params, data=data, cookies=cookies)
if not r3.ok:
    raise Exception(f"Status Code: {r3.status_code}")
bs = BeautifulSoup(r3.text, "html.parser")
downloadables = [soup["href"] for soup in bs.find_all('a')]
downloadables.pop()

print(f'\tRaw Video URL: {downloadables[-1]}')
r4 = requests.get(downloadables[-1], headers=headers)
if not r4.ok:
    raise Exception(f"Status Code: {r4.status_code}")

# Create output path
os.makedirs(out_path, exist_ok=True)

# Download video
with open(out_name, 'wb') as f:
    for chunk in r4.iter_content(chunk_size = 1024*1024):
        if chunk:
            f.write(chunk)

print("\n[!] Done")
