'''
Created on Dec 27, 2015

@author: mhemenway
'''
import quip
import json
import config

token = config.quip_token
folder_find = 'aproximatebible'

client = quip.QuipClient(token)

def find_quip_folder(folder_name):
    '''
    Returns as a string the id of the first folder instance found that matches the name passed.
    Assumes client connection already established.
    '''
    user = client.get_authenticated_user()
    
    desktop = client.get_folder(user['desktop_folder_id'])
    desktop_threads = desktop['children']
    
    folder_ids = [thread['folder_id'] for thread in desktop_threads if 'folder_id' in thread]
    
    for folder_id in folder_ids:
        folder = client.get_folder(folder_id)
        if folder['folder']['title'].lower() == folder_name.lower():
            return folder['folder']['id']

# test = find_quip_folder(folder_find)
# print test

thread = client.get_thread('NCkfAroUWSd6')
# print thread['html']
message_rich = json.dumps([['body','This is a <a href=\'http://www.google.com\'>link</a>']])
message = client.new_message('NCkfAroUWSd6', parts=message_rich, section_id='OXGACAWxdeM')