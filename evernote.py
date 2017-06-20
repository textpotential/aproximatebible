'''
Created on Dec 15, 2015

@author: mhemenway
'''
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import config

client = EvernoteClient(token=config.evernote_token, sandbox=False)
note_store = client.get_note_store()

note_filter = NoteFilter(words='intitle:reading interfaces')
note_spec = NotesMetadataResultSpec(includeTitle=True)
note_list = note_store.findNotesMetadata(config.evernote_token, note_filter, 0, 1, note_spec)

content = note_store.getNoteContent(note_list.notes[0].guid)

print(content)

start_char = content.find('<en-note>') + len('<en-note>')
end_char = content.find('</en-note>')

trim_content = content[start_char:end_char]
