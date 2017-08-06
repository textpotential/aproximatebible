import os
import re
import fileinput


def change_file_extension():

    dir_ = 'docs/_posts'
    post_filenames = os.listdir(dir_)

    for filename in post_filenames:
        print(filename.replace('.md', '.html'))


file = '/Users/mhemenway/git/bai/chapt1.md'


def translate_footnotes(filepath):

    '''
    - find all ^[...] and put in container with brackets stripped
    - replace with [^#]
    - move to first line break, add break and add leader [^#]:

    '''

    with open(filepath, mode='r', encoding='utf-8') as f:

        text = f.read()

    note_pattern = re.compile(r'(\^\[)((\[.*?\])|(.*?))(\])(.*?)(?=\^\[|$)',
                              flags=re.DOTALL)

    notes_w_ref = []

    for i, note in enumerate(note_pattern.findall(text)):
        # print(note_pattern.findall(text)[0])
        ref = '[^{num}]:'.format(num=str(i))
        note_text = note[1]
        notes_w_ref.append(ref + ' ' + note_text)

    new_text = note_pattern.sub(build_ref, text)

    return new_text + ('\n\n'.join(notes_w_ref))


def build_ref(s):

    if not hasattr(build_ref, 'counter'):
        build_ref.counter = 0

    ref = '[^{number}]'.format(number=build_ref.counter) + s.group(6)

    build_ref.counter += 1

    return ref


print(translate_footnotes(file))
