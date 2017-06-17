'''
Created on Mar 26, 2016

@author: mhemenway
'''

import requests
# import pagerank_vector
from bs4 import BeautifulSoup
import json
import config


def get_post_text(url):

    request = requests.get(url)
    full_html = request.content
    soup = BeautifulSoup(full_html, 'html.parser')
    post_text = soup.find('div', class_='post-content')

    return post_text.text


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
                post_text = get_post_text(trunk + rel_url)
                posts.append(post_text)

    return posts


def get_disqus_comments(forum, public_key):

    disqus_url = ('https://disqus.com/api/3.0/posts/list.json?' +
                  'limit=100' +
                  '&api_key=' + public_key +
                  '&forum=' + forum)

    has_next = True
    comments = []
    url = disqus_url

    while has_next:

        request = requests.get(url)
        json_string = (request.content.decode('utf-8'))
        json_posts = json.loads(json_string)

        for item in json_posts['response']:
            comments.append(item['raw_message'])

        if json_posts['cursor']['hasNext']:
            cursor = json_posts['cursor']['next']
            url = disqus_url + '&cursor=' + cursor
            has_next = True
        else:
            has_next = False

    return comments


# comments = get_disqus_comments('aproximatebible', config.disqus_token)

# for comment in comments:
#     print(comment)

# print(len(comments))


posts = get_posts('http://aproximatebible.postach.io')

all_posts = ' '.join(posts)

# posts_comments = all_posts + ' '.join(comments)

# pagerank_vector.get_highest_pagerank_scores(posts_comments, 5)

# for post in posts:
#     print(post)
#
# print(len(posts))
print(len(all_posts.split()))

# print(len(urls))
#
# for url in urls:
#     print(url)
