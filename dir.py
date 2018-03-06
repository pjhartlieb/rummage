#!/usr/bin/python

import os
import re

target_files=[]
for root, directories, filenames in os.walk('/path/to/directory/'):
	for filename in filenames:
		fullName=os.path.join(root,filename)
		#print filename
		if re.match(r'.*page.html$',fullName) and re.match(r'.*/adminstrative/.*|.*/technical/.*|.*/physical/.*',fullName):
			file_number=len(target_files)
			fullName=os.path.join(root,filename)
			target_files.append(fullName)
			print file_number

for i in target_files:
	print i
