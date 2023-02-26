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
with requests.Session() as s:
    r0 = s.get(link, timeout=timeout, headers=headers)
    bs = BeautifulSoup(r0.text, 'html.parser')
    # print(bs.prettify())
    # sys.exit(0)

    # Get video meta data
    meta = re.search('{.*AppContext.*}', bs.prettify()).group()
    meta = json.loads(meta)
    video_url  = meta['SEO']['canonical']
    print(video_url)

    # Get download meta data
    r1 = s.get(video_url, timeout=timeout, headers=headers, cookies=s.cookies)
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

    # Request video data
    print(f'\n[+] dl_addr = {dl_addr}\n')
    r2 = s.get(dl_addr, timeout=timeout, headers=headers, cookies=s.cookies)

    if not r2.ok:
        raise Exception(f"Status Code is {r2.status_code}")

    # Create output path
    os.makedirs(out_path, exist_ok=True)

    # Download video
    with open(out_name, 'wb') as f:
        for chunk in r2.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
