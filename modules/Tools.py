#! /usr/bin/env python3

# Author:       Author
# Date:         July 04 2022 at 06:42:41 PM
# Description:  Create a gallery from a list of images/links

import os

HTML_SCROLLABLE = '''
<!-- NOTE: TAG img MUST BE IN LINE -5 -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Gallery</title>
        <style>
            body, img{
                padding: 0;
                margin: 0;
                border: 0;
                text-align: center;
                font-size: 0;
            }

            img{
                width: 74%;
            }

           @media only screen and (max-width: 1080px) {
                img{
                    width: 100%;
                }
            }
        </style>
    </head>
    <body bgcolor="#131315">

    <img src="img-holder"></img>

    </body>
</html>
'''

HTML_GRID = '''
<!-- NOTE: TAG div class="imgbox" MUST BE IN LINE -5 -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Gallery</title>
        <style>
            body, img{
                padding: 0;
                margin: 0;
                border: 0;
                text-align: center;
                font-size: 0;
            }

            div.parent{
                width: 100%;
                height: auto;
                margin: 0px;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }

            div.imgbox {
                float: left;
                width: 200px;
                height: 200px;
                display: flex;
                overflow: hidden;
                border:solid 1px #fff;
                background-repeat: no-repeat;
                background-position: center center;
                background-size: cover;
                margin: 8px;
                border-radius: 16px;
            }

            a{
                width: 100%;
                height: 100%;
            }

            @media only screen and (max-width: 1080px) {
                 div.imgbox{
                     width: 180px;
                     height: 180px;
                 }
             }
        </style>
    </head>
    <body bgcolor="#131315">
    <nav>
        <div class="parent">
            <div class="imgbox" style='background-image: url("img-holder")'> <a target="_blank" href="img-holder"></a> </div>
        </div>
    </body>
</html>
'''

IMAGE_HOLDER = 'img-holder'

''' TODO:
Input:
    chapters_path
Structute:
    chapters_path/chapter-n/image-n.jpg
                 |L1       |
                           |L2
Make the levels flexible [sync w/ ../create_json.py]
    L = 2 -> L = n
'''

def scrollable(chapters_path, output_path='.'):
    holder = HTML_SCROLLABLE.split('\n')[-5]
    for chapter in os.listdir(chapters_path):
        imgs = ''
        for page in sorted(os.listdir('{}/{}'.format(chapters_path, chapter))):
            if not (page.split('.')[-1].lower() in ['jpeg', 'jpg', 'png']):
                continue
            imgs = imgs + holder.replace(IMAGE_HOLDER, page)
        with open('{}/{}/scroll.html'.format(chapters_path, chapter), 'w') as f:
            f.write( HTML_SCROLLABLE.replace(holder, imgs + '\n') )

    print('file://{}/{}/'.format(os.getcwd(),chapters_path))
    # print('http://0.0.0.0:8080/')

def grid(chapters_path, output_path='.'):
    holder = HTML_GRID.split('\n')[-5]
    for chapter in os.listdir(chapters_path):
        imgs = ''
        for page in sorted(os.listdir('{}/{}'.format(chapters_path, chapter))):
            if not (page.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']):
                continue
            imgs = imgs + holder.replace(IMAGE_HOLDER, page)
        with open('{}/{}/grid.html'.format(chapters_path, chapter), 'w') as f:
            f.write( HTML_GRID.replace(holder, imgs + '\n') )

    print('file://{}/{}/'.format(os.getcwd(),chapters_path))
    # print('http://0.0.0.0:8080/')
