'''
Need to look in all of the HTML files and find img tags with
'postachio-images' in the url and download the file and then 
replace the src with assets/images/[filename]
'''

import re
import os
from bs4 import BeautifulSoup
import requests


def get_images(html):

    image_urls = []

    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.findAll('img', src=re.compile(r'postachio-images')):
    #    img_link = parse.urljoin(base_url, img['src'])
        img_link = img['src']

        if img_link not in image_urls:
            image_urls.append(img_link)
            save_web_file(img_link, 'postachio_html/images')
            # print(img_link)


def save_web_file(url, path):

    filename = url.rsplit('/', 1)[-1]
    fullpath = os.path.join(path, filename)

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(fullpath, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def change_img_src(soup, path):

	for img in soup.findAll('img', src=re.compile(r'postachio-images')):
		orig_src = img['src']
		filename = orig_src.rsplit('/', 1)[-1]
		new_src = path + filename
		img['src'] = new_src

	return soup


html_path = 'postachio_html'
# filename = 'anarchic-approximations.html'

# This is what I used to replace image source with new path to images in assets directory

for filename in os.listdir(html_path):

	if filename.endswith('.html'):
		
		fullpath = os.path.join(html_path, filename)
		
		with open(fullpath, mode='r+', encoding='utf-8') as f:
			file_contents = f.read()
			soup = BeautifulSoup(file_contents, 'html.parser')
			new_soup = change_img_src(soup, '/assets/article_images/')
			if new_soup:
			    f.seek(0)
			    f.write(str(new_soup))
			    f.truncate()
