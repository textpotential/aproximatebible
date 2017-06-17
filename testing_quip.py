'''
Created on Dec 20, 2015

@author: mhemenway
'''

import requests
import quip
from bs4 import BeautifulSoup
import json
import config

url = 'http://aproximatebible.postach.io/post/translating-copyright'
request = requests.get(url)
full_html = request.content

# use beautifulsoup to select just the title and post content to send to quip 
soup = BeautifulSoup(full_html,'html.parser')

# i need to get section that is blockquote and the end of immediately preceding section.
# first attempt is to simply append Aside or Class in italics to each blockquote item  
def flag_notes(raw_soup):
    notes = raw_soup.find_all('blockquote')    
    
    for note in notes:
        aside = raw_soup.new_tag("i")
          
        if 'class' not in note.attrs:
            aside.string = "ASIDE: "
        else:
            aside.string = note['class'][0].upper() + ': '
            
        note.p.next_element.insert_before(aside)
        
    return raw_soup
    
flagged_soup = flag_notes(soup)

post_html = flagged_soup.find('div',class_='post-content')

#print post_html
# embeds = post_html.find_all('iframe')
# 
# for each_iframe in post_html.find_all('iframe'):
#     
#     src = each_iframe['src'].strip()
#     print src
#     link = flagged_soup.new_tag('a',href=src)
#     link.string = src
#     print each_iframe
#     each_iframe.replace_with(link)
#     
# print post_html.find_all('a')
# print post_html.find_all('iframe')   

client = quip.QuipClient(config.quip_token)
quip_thread = client.new_document(post_html,title='testing2')
#quip_thread = client.get_thread('QE4qA5oQdGba')

#def translate_notes(quip_thread):
    
thread_id = quip_thread['thread']['id']    
new_soup = BeautifulSoup(quip_thread.get('html', None),'html.parser')
 
comments = new_soup.find_all('i',string='ASIDE: ')
 
for comment in comments:
    print comment.find_parent('p').find_previous(id=True)['id']
    print comment.find_parent('p').find_previous_sibling('p')
    section_id = comment.find_parent('p').find_previous_sibling('p')['id']
    comment_id = comment.find_parent('p')['id']
    #comment.extract()
    #comment_html = str(new_soup.find(id=comment_id))    
    #comment_parts = json.dumps([['body',comment_html]])
    
#print quip_thread.get('html', None)
#         client.new_message(thread_id,parts=comment_parts,silent=True,section_id=section_id)
#         client.edit_document(thread_id, '', operation=5, section_id=comment_id)

#translate_notes(new_thread)