#! /usr/bin/env python3

# Author:       Author
# Date:         July 05 2022 at 12:23:16 PM
# Description:  Menu for the gallery

import os
import json

head = 'handmade/custom'
# head = 'manga'
cwd = os.getcwd()
path = os.path.join(cwd, head)

'''
L1: Titles
L2: Chapters
L3: Html
'''

titles = os.listdir(path)
structure = { }

for file in os.listdir(path):
    path_l1 = os.path.join(path, file)
    if not os.path.isdir(path_l1):
        continue
    # print('\nL1: ' + file)
    html_files = {'grid': [], 'scroll': []}
    for ch in sorted(os.listdir(path_l1)):
        path_l2 = os.path.join(path_l1, ch)
        if not os.path.isdir(path_l2):
            continue
        # print('L2: ' + ch)
        for html in os.listdir(path_l2):
            path_l3 = os.path.join(path_l2, html)
            if os.path.isdir(path_l3):
                continue
            if html.split('.')[-1].lower() == 'html':
                if html.split('.')[-2].lower() == 'grid':
                    html_files['grid'].append('http://localhost:8080/' + os.path.join(head, file, ch, html))
                else:
                    html_files['scroll'].append('http://localhost:8080/' + os.path.join(head, file, ch, html))
    structure[file] = {'chapters': html_files}

with open(os.path.join(path, 'menu.json'), 'w') as f:
    f.write(json.dumps(structure, indent=4))

print('http://localhost:8080/{}/menu.json'.format(head))
