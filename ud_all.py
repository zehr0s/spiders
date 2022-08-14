#! /usr/bin/env python3

# Author:       Author
# Date:         August 13 2022 at 02:24:14 PM
# Description:  Updates all the menus and galleries if necessary

import os
import json
from modules.Tools import start_server
from modules.Tools import create_menu
from modules.Tools import scrollable
from modules.Tools import grid

''' Variables '''
roots= [
    'handmade/custom',
    'handmade/manhwa365',
    'handmade/zahard',
    'manga'
]

print('== Updated ==')
grid('handmade/custom/downloads')
grid('handmade/manhwa365/chapters')
grid('handmade/zahard/chapters')
print()

for root in roots:
    create_menu(root, 'menus', levels=2)

op = input('\nStart server [Y/N]: ')
print()

if op.lower() == 'y':
    start_server()
