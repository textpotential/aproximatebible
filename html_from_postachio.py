'''
- Get HTML (done)
- get title for filename (done)
??- convert html of content to markdown (github)
- download all images (done)
- translate image URLs to local theme (done)
- migrate disqus 
- move posts to _posts and images to assets/images
- translate heading with dates etc. 
- translate relative links and links to postachio
'''

import requests
import re
from bs4 import BeautifulSoup
import pypandoc

url = 'http://aproximatebible.postach.io'

# request = requests.get(url)
# full_html = request.content
# soup = BeautifulSoup(full_html, 'html.parser')
# post_text = soup.find('div', class_='post-content')

# print(post_text.children)


def get_posts(trunk):

    toc_url = trunk + '/{num}'
    pg_num = 1
    has_posts = True
    posts = []

    while has_posts:

        page_url = toc_url.format(num=pg_num)
        # print(toc_url)
        request = requests.get(page_url)
        full_html = request.content
        soup = BeautifulSoup(full_html, 'html.parser')

        post_links = soup.find_all('p', class_='post-link')

        if not post_links:
            has_posts = False
        else:
            has_posts = True
            pg_num = pg_num + 1

            for post in post_links:
                rel_url = post.a.attrs['href']
                # urls.append(trunk + rel_url)
                # post_text = get_post_text(trunk + rel_url)
                posts.append(rel_url)

    return posts


def urlify(s):

    # Trim all white space before and after the string
    s = s.strip()

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s


def write_post_to_file(url):

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    post_html = soup.find('div', class_='post-content')

    # get post title for filename and format it
    post_head = post_html.find('header')
    post_title = post_head.text.strip()
    filename = urlify(post_title)

    # write html to file
    folder = 'postachio_html/'
    with open(folder + filename + '.html', mode='w', encoding='utf-8') as f:

        f.write(str(post_html))


def build_header(html):

    soup = BeautifulSoup(html, 'html.parser')

    # get post title for header
    post_head = soup.find('header')
    post_title = post_head.text.strip()

    # get post date
    date_p = soup.find('p', class_='post-date')
    time_tag = date_p.find('time')
    date_time = time_tag['datetime']

    # get first local image
    img_tag = soup.find('img', src=re.compile(r'^/'))
    if img_tag:
        img_src = img_tag['src']
        image_line = 'image:\t' + img_src
    else:
    	image_line = ''

    # construct jekyll header from variables
    vars = {'title': post_title, 'date': date_time, 'image': image_line}
    header = '---\nlayout:\tpost\ntitle:\t{title}\ndate:\t{date}\n{image}\n---'
    full_header= header.format(**vars)

    return full_header


with open('postachio_html/Codex-all-the-way-down.html', mode='r', encoding='utf-8') as f:
	contents = f.read()
	head = build_header(contents)
	# print(head)

	soup = BeautifulSoup(contents, 'html.parser')
	soup.div.unwrap()
	soup.header.decompose()
	soup.p.decompose()

	pdoc_args = ['--atx-headers', '--smart']
	md_post = pypandoc.convert_text(str(soup), to='md', format='html', extra_args=pdoc_args)
	print(head+ '\n' + md_post)

# Run these lines to get all the HTML from the site.

# post_urls = get_posts(url)

# for post_url in post_urls:

#     write_post_to_file(url + post_url)

# get one post
# a = write_post_to_file('http://aproximatebible.postach.io/post/codex-all-the-way-down')

'''
- get title (done)
- get post date (done)
- get first image src (done)
- build header for post (done)
- remove first div, header and p object. 
-- soup remove these objects
- use pandoc to convert HTML to MD in new file
-- pypandoc convert-text to MD with --smart and --atx-headers args
-- write header to file and then converted MD content
'''