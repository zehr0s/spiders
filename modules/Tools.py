#! /usr/bin/env python3

# Author:       Author
# Date:         July 04 2022 at 06:42:41 PM
# Description:  Create a gallery from a list of images/links

import os

def scrollable(chapters_path, output_path='.'):
    html = """
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
    holder
    </body>
    </html>
    """

    for chapter in os.listdir(chapters_path):
        imgs = ''
        for page in sorted(os.listdir('{}/{}'.format(chapters_path, chapter))):
            if not (page[-3:].lower() in ['jpg', 'png']):
                continue
            imgs = imgs + '\n    <img src="{}"></img>'.format(page)
        with open('{}/{}/scroll.html'.format(chapters_path, chapter), 'w') as f:
            f.write( html.replace('holder', imgs + '\n') )

    print('file://{}/{}/'.format(os.getcwd(),chapters_path))
    # print('http://0.0.0.0:8080/')

def grid(chapters_path, output_path='.'):
    html = """
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
                    height: auto;
                    width: auto;
                    display: flex;
                }

                nav{
                    width: 80%;
                    display: inline-block;
                }

                div.imgbox {
                    float: left;
                    width: 300px;
                    height: 300px;
                    line-height: 300px;
                    overflow: hidden;
                    border:solid 1px #fff;
                    text-align: center;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                div.parent{
                    width: 100%;
                    height: auto;
                    float: left;
                    align-self: center;
                    text-align: center;
                    margin: 0 auto;
                    position: relative;
                    display: flex;
                    flex-direction: row;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: center;
                }

                @media only screen and (max-width: 1080px) {
                     div.imgbox{
                         width: 180px;
                         height: 180px;
                     }
                     nav{
                         width: 100%;
                     }
                 }
            </style>
        </head>
        <body bgcolor="#131315">
        <nav>
            <div class="parent">
                holder
            </div>
        </body>
    </html>
    """

    template = """
                <div class="imgbox">
                    <a target="_blank" href="image-holder"><img src="image-holder"></img></a>
                </div>
    """

    for chapter in os.listdir(chapters_path):
        imgs = ''
        for page in sorted(os.listdir('{}/{}'.format(chapters_path, chapter))):
            if not (page[-3:].lower() in ['jpg', 'png']):
                continue
            imgs = imgs + '\n' + template.replace('image-holder', page)
        with open('{}/{}/scroll.html'.format(chapters_path, chapter), 'w') as f:
            f.write( html.replace('holder', imgs + '\n') )

    print('file://{}/{}/'.format(os.getcwd(),chapters_path))
    # print('http://0.0.0.0:8080/')
