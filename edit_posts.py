import os
import re

dir_ = 'docs/_posts'
post_filenames = os.listdir(dir_)

for filename in post_filenames:

    if filename.endswith('.md'):

        fullpath = os.path.join(dir_, filename)

        with open(fullpath, mode='r', encoding='utf-8') as f:
            contents = f.read()

        # truncate filename in list after 3rd dash and before dot
        # search for that truncated filename anywhere in file and replace with
        # full filename minus .md 
        # rewrite contents to file

        # for filename in post_filenames:
        #     post_url = os.path.splitext(filename)[0]
        #     post_trunc = post_url.split('-', 3)[3]

        #     old_ref = 'post_url ' + post_trunc.lower()
        #     new_ref = 'post_url ' + post_url

        #     contents = contents.replace(old_ref, new_ref)

        
        # contents = contents.replace('%}', '%}{% endraw %}')
        # contents = contents.replace('{% post_url', '{% raw %}{% post_url')

        contents = contents.replace('{% raw %}', '')
        contents = contents.replace('{% endraw %}', '')
        # print(contents)

        with open(fullpath, mode='w', encoding='utf-8') as g:
            g.write(contents)



            # if new_soup:
            #     f.seek(0)
            #     f.write(str(new_soup))
            #     f.truncate()
