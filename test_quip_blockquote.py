'''
Created on May 17, 2016

@author: ubuntu
'''
import postachio_to_quip
from bs4 import BeautifulSoup
import quip
import config

url = 'http://aproximatebible.postach.io/post/interfacing-religion'
folder = 'testing'

client = quip.QuipClient(config.quip_token)

user = client.get_authenticated_user()
desktop_folder_id = client.get_folder(user['desktop_folder_id'])

#print thread['ZeFAAAPFArH']['html']

print desktop_folder_id

# html = postachio_to_quip.translate_html(url)
#  
# notes = html.find_all('blockquote')
# 
# for note in notes:
#     print note


