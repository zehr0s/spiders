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
link = ''
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/5311 (KHTML, like Gecko) Chrome/40.0.821.0 Mobile Safari/5311'}

''' Main '''
r = requests.post(link, timeout=timeout, headers=headers)
bs = BeautifulSoup(r.text, 'html.parser')
# Get source link
for k, target in enumerate(bs.find_all('link')):
    if not ('www.tiktok.com' in target['href']):
        continue
    print(target['href'])
    break

# Get video meta data
r = requests.get(target['href'], timeout=timeout, headers=headers)
#r = requests.get(target['href']+'?lang=es', timeout=timeout, headers=headers)
# print(r.ok, target['href'])
#print( bs.prettify() )
meta = re.search('{.*downloadAddr.*}', bs.prettify()).group()
meta = json.loads(meta)
id = list(meta['ItemModule'].keys())[0]
author = meta['ItemModule'][id]['author']
v_format = meta['ItemModule'][id]['video']['format']
v_quality = meta['ItemModule'][id]['video']['videoQuality']
v_definition = meta['ItemModule'][id]['video']['definition']
dl_addr = meta['ItemModule'][id]['video']['playAddr']
print(dl_addr)

# Request video data
r = requests.get(dl_addr, timeout=timeout, headers=headers)
if not r.ok:
    sys.exit(0)

# Create output path
os.makedirs(out_path, exist_ok=True)
out_path = os.path.join(out_path, author)
os.makedirs(out_path, exist_ok=True)

# Download video
with open(os.path.join(out_path, '{}-{}-{}.{}'.format(id, v_quality, v_definition, v_format.lower())), 'wb') as f:
    for chunk in r.iter_content(chunk_size = 1024*1024):
        if chunk:
          f.write(chunk)
