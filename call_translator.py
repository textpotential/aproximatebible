'''
Created on Feb 5, 2016

@author: mhemenway
'''

import postachio_to_quip
import config

url = 'http://aproximatebible.postach.io/post/interfacing-religion'
folder = 'testing'

postachio_to_quip.translate_to_quip(url, config.quip_token, folder)
