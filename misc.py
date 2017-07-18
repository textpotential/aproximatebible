import os
import re

dir_ = 'docs/_posts'
post_filenames = os.listdir(dir_)

for filename in post_filenames:
	print(filename.replace('.md','.html'))