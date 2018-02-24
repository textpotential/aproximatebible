import requests
from pprint import pprint

api_token = 'ZWwpJsx9xM9GrFf5nsMTNNKUUUmISu3DjsandtkO'
pass_fake = 'X'

verse_endpoint = 'https://bibles.org/v2/verses.js?keyword=book'
verse_resp = requests.get(verse_endpoint, auth=(api_token, pass_fake))
verses = verse_resp.json()

pprint(verses)