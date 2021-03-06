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
import urllib
import os

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


def build_header(soup):

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


def make_jekyll_filename(soup):

    # get post title for filename
    post_head = soup.find('header')
    post_title = post_head.text.strip()
    file_title = urlify(post_title)

    # get post date
    date_p = soup.find('p', class_='post-date')
    time_tag = date_p.find('time')
    date_time = time_tag['datetime']
    date = re.match(r'.+?(?=\s)', date_time)

    filename = date.group(0) + '-' + file_title + '.md'

    return filename


def trans_rel_links(soup):

    rel_as = soup.find_all('a', href=re.compile(r'^/'))
    for rel_a in rel_as:
        beg_href = rel_a['href']
        name = re.sub('/', '', beg_href)
        new_href = '{{{{site.baseurl}}}}{{% post_url {file_name} %}}'.format(file_name=name)
        rel_a['href'] = new_href

    return soup


def html_2_md(html, new_path):

    soup = BeautifulSoup(html, 'html.parser')

    head = build_header(soup)
    post_filename = make_jekyll_filename(soup)

    soup.div.unwrap()
    soup.header.decompose()
    soup.p.decompose()

    soup_b = trans_rel_links(soup)

    pdoc_args = ['--atx-headers', '--smart']
    md_post = pypandoc.convert_text(str(soup_b), to='markdown_github', format='html', extra_args=pdoc_args)

    full_post = head + '\n' + urllib.parse.unquote(md_post)

    with open(new_path + post_filename, mode='w', encoding='utf-8') as g:
        g.write(full_post)

    return post_filename


html_path = 'postachio_html'

for filename in os.listdir(html_path):

    if filename.endswith('.html'):

        fullpath = os.path.join(html_path, filename)

        with open(fullpath, mode='r', encoding='utf-8') as f:
            contents = f.read()

        new_file = html_2_md(contents, 'docs/_posts/')
        print(new_file)

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
- build filename from date and title (done)
- remove first div, header and p object. (done)
-- soup remove these objects
- use pandoc to convert HTML to MD in new file (done)
-- pypandoc convert-text to MD with --smart and --atx-headers args (done)
-- write header to file and then converted MD content
'''