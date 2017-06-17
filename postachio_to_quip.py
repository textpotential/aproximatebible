'''
Created on Dec 18, 2015

@author: mhemenway

Things to add:
    - check for existing doc of same title and abort if found
    
'''

import requests
import quip
from bs4 import BeautifulSoup
import json

def flag_blockquotes(raw_soup):
    '''
    This function takes a beautifulsoup object and prefixes all blockquote tags 
    with the first class attribute in the blockquote tag or ASIDE if none. This
    is necessary because quip has no built-in formatting for blockquotes.
    '''
    notes = raw_soup.find_all('blockquote')

    for note in notes:
        aside = raw_soup.new_tag("i")
          
        if 'class' not in note.attrs:
            aside.string = "ASIDE: "
        else:
            aside.string = note['class'][0].upper() + ': '
          
        note.p.next_element.insert_before(aside)
    
    return raw_soup 

def translate_html(post_url):
    '''
    This function takes a url from postach.io and translates the html into a 
    vernacular that works better in quip.
    '''
    
    # get HTML from postach.io URL using gridley theme and run through beautiful soup
    request = requests.get(post_url)
    full_html = request.content
    soup = BeautifulSoup(full_html,'html.parser')
    
    # use function to add prefix to all blockquote tags
    flagged_soup = flag_blockquotes(soup)
    
    # select just the post content from the page 
    post_html = flagged_soup.find('div',class_='post-content')
    
    # add URL to first header which will be used as title for quip doc.
    post_html.h1.string.wrap(flagged_soup.new_tag('a',href=post_url))
    
    # expand url for relative links to other posts in site using the trunk of the passed 
    # url parameter
    rel_links = post_html.select('a[href^="/"]')
    
    for link in rel_links:
        link['href'] = post_url.rsplit('/',1)[0] + link['href']
        
    # replace all iframe tags with a link to just src URL
    for each_iframe in post_html.find_all('iframe'):
    
        src = each_iframe['src'].strip()
        link = flagged_soup.new_tag('a',href=src)
        link.string = src
        each_iframe.replace_with(link)
        
    return post_html

def find_quip_folder(folder_name,quip_client):
    '''
    Returns as a string the id of the first folder instance found that matches the name passed.
    Assumes client connection already established.
    '''
    user = quip_client.get_authenticated_user()
    
    desktop = quip_client.get_folder(user['desktop_folder_id'])
    desktop_threads = desktop['children']
    
    folder_ids = [thread['folder_id'] for thread in desktop_threads if 'folder_id' in thread]
    
    for folder_id in folder_ids:
        folder = quip_client.get_folder(folder_id)
        if folder['folder']['title'].lower() == folder_name.lower():
            return folder['folder']['id']

def translate_notes(quip_thread,quip_client):
    '''
    Converts the blockquotes marked with ASIDE by the flag_blockquotes function into
    quip conversation messages linked to the immediately previous section in the document and removes
    the ASIDEs from the body of the document.
    '''
    thread_id = quip_thread['thread']['id']    
    new_soup = BeautifulSoup(quip_thread.get('html', None),'html.parser')
     
    comments = new_soup.find_all('i',string='ASIDE: ')
     
    for comment in comments:
        section_id = comment.find_parent('p').find_previous(id=True)['id']
        comment_id = comment.find_parent('p')['id']
        comment.extract()
        comment_html = str(new_soup.find(id=comment_id))    
        comment_parts = json.dumps([['body',comment_html]])
        
        quip_client.new_message(thread_id,parts=comment_parts,silent=True,section_id=section_id)
        quip_client.edit_document(thread_id, '', operation=5, section_id=comment_id)

def translate_to_quip(url,quip_token,quip_folder):
    '''
    Assembles the functions in this module and initiates the quip client. 
    '''
    # set url to translate and call translate function
    translated_html = translate_html(url)
    
    # establish quip connection, find folder id and send translated post to quip as new doc.
    client = quip.QuipClient(quip_token)
    folder_id = find_quip_folder(quip_folder,client)
    new_thread = client.new_document(translated_html,member_ids=[folder_id])
    #translate_notes(new_thread,client)
    return new_thread