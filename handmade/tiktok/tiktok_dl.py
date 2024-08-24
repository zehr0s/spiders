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

try:
    # Get video meta data
    meta = re.search('{.*seo\.abtest.*}', bs.prettify()).group() # AppContext
    meta = json.loads(meta)
    # print(json.dumps(meta, indent=4))
    # with open('data.json', 'w') as f:
    #     f.write(json.dumps(meta))
    video_url  = meta['__DEFAULT_SCOPE__']['seo.abtest']['canonical']
except KeyError:
    video_url = link
except Exception as e:
    raise e

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
        '[+] Downloading {}:\n\tUser: {}\n\tVideo ID: {}\n\tQuality: {}\n\tDefinition: {}\n\tFormat: {}'
        .format(out_name, author, id, v_quality, v_definition, v_format.lower())
    )
except:
    # Print info
    id = video_url.split('/')[-1]
    author = video_url.split('/')[-3][1:]
    if mobile:
        out_name = os.path.join(out_path, '{}-{}.{}'.format(author,id,'mp4'))
    else:
        out_path = os.path.join(out_path, author)
        out_name = os.path.join(out_path, '{}.{}'.format(id,'mp4'))
    print(
        '[+] Downloading {}:\n\tUser: {}\n\tVideo ID: {}'
        .format(out_name, author,id)
    )

# Request video download url
headers = {
    'Host': 'lovetik.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/5311 (KHTML, like Gecko) Chrome/40.0.821.0 Mobile Safari/5311',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,es;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': '''cf_clearance=t1eHmdsTkkO8fwgLyI59Hpe.v5hGbHHAaWnr3LpaFFI-1724521842-1.2.1.1-ET7orf_OIKbZvv8_MAW3HqHpJJsDSxvx4wNiOQPuq5KDsrBBNcTMWxZffV54K2xCQhHN6dS6ELKa3dPtb7NT.IwgX1iUsjTbygZhgM_4XBKN4oyOOe8nRtnjbsocVXWukcPf5ZHtQfItNpBc.lQYQ2GFobS409SBUCN7JDfft.tnqD6F1KoMfjCAH54FDeJG9yATBR_pbdcc8r4zMCCaeG5Cbx.yiaAzXQ2lfHmrmFSc1Y4SeEHn4R3rTL3fkz.GRFxJ7KKUS7BSlTpBpdPKhS.rz2j7gq8PrErfkMCKHllv1f5TCPOFzroKOWdxC6yw7W9cs1_jBtYbdn66kANb_Nv2fpIadJbNjXOYq6EHI_o7AjrJnjOdtgCUx5J5ODLj''',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers'
}

data = {
    'query': link # f'https://www.tiktok.com/@{author}/video/{id}'
}

scrap_url = "https://lovetik.com/api/ajax/search"
retries = 10
for i in range(retries):
    n = i+1
    print(f'[+] Attempt ({n}/{retries}) at scraping {scrap_url}/q={data["query"]}')
    try:
        r_aux = requests.post(scrap_url, data=data, headers=headers, timeout=timeout)
    except Exception as e:
        if n == retries:
            raise e
        continue
    break

links = []
if r_aux.ok:
    result = json.loads(r_aux.text)
    for link in result['links']:
        if 'mp4' in link['t'].lower():
            links.append({'size':link['s'].lower(),'link':link['a']})
else:
    raise Exception(f"No link found: {r_aux.ok}")

for i, downloadable in enumerate(links[::-1]):
    try:
        print(f'\tAttempt ({i+1}) at metadata {downloadable["size"]}')
        r4 = requests.get(downloadable['link'], timeout=timeout, stream=True)
    except:
        print(r4.ok,r4.text)
        continue
    if r4.ok:
        break
    else:
        continue

# Create output path
os.makedirs(out_path, exist_ok=True)

# Download video
total_size = int(r4.headers.get('content-length', 0))
downloaded_size = 0
with open(out_name, 'wb') as f:
    for chunk in r4.iter_content(chunk_size = 1024*1024):
        if chunk:
            f.write(chunk)
            downloaded_size += len(chunk)
        print(f"[+] Progress: {downloaded_size}/{total_size} ({100*(downloaded_size/total_size):.2f}%)")
