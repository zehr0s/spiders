#! /usr/bin/env python3

# Author:       Author
# Date:         July 04 2022 at 06:42:41 PM
# Description:  Create a gallery from a list of images/links

import os
import json
import http.server
import socketserver


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

# TODO: Combine scrollable & grid into one function w/ options to create either one or both
def scrollable(chapters_path):
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

def grid(chapters_path):
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

# TODO: Format the .json menu & order in human readable format
def create_menu(root, output_path='.', levels=2, local=False):
    last_heads = [root]
    root_web = os.getcwd() if local else 'http://localhost:8080/'
    structure = {}
    for level in range(levels):
        new_heads = []
        for head in last_heads:
            if level == levels-1:
                structure[head] = {}
            # html_files = {'grid': [], 'scroll': []}
            for entry in sorted(os.listdir(head)):
                if not os.path.isdir(os.path.join(head, entry)):
                    continue
                new_heads.append(os.path.join(head, entry))
                if level == levels-1:
                    structure[head][new_heads[-1]] = []
                    for html in os.listdir(new_heads[-1]):
                        html_path = os.path.join(new_heads[-1], html)
                        if os.path.isdir(html_path):
                            continue
                        if html.split('.')[-1].lower() == 'html':
                            '''
                            if html.split('.')[-2].lower() == 'grid':
                                html_files['grid'].append(
                                    'http://localhost:8080/' + os.path.join(new_heads[-1], html))
                            else:
                                html_files['scroll'].append(
                                    'http://localhost:8080/' + os.path.join(new_heads[-1], html))
                            '''
                            structure[head][new_heads[-1]].append(
                                os.path.join(root_web, new_heads[-1], html)
                            )
            #if level == levels-1:
            #    structure[head] = {'chapters' : html_files}
        last_heads = new_heads

    os.makedirs(output_path, exist_ok=True)
    out_name = os.path.join(output_path, 'menu-{}.json'.format(root.replace('/', '-')))
    with open(out_name, 'w') as f:
        f.write(json.dumps(structure, indent=4))
    print('[+] {}'.format(out_name))

# TODO: Combine create_menu w/ grid & scrollable
def create_all():
    pass

class __SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/up':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'up')
        else:
            super().do_GET()


# TODO: Debug close properlly
def start_server(port=8080):
    httpd = socketserver.TCPServer(('', port), __SimpleHTTPRequestHandler)
    print('Server started on http://localhost:{}'.format(port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    httpd.shutdown()

    print('\n[!] Server stopped.')

