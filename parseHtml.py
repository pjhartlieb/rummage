#!/usr/bin/python

from bs4 import BeautifulSoup
import os

# [*] read in file names to list and strip off whitespace and \n

with open("files.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]

# [*] parse each file and pull out the names
masterMatrix=[]

for sourceFile in content:
	opensourceFile=open(sourceFile)
	soup=BeautifulSoup(opensourceFile, "html.parser")
	nameChunks = soup.find_all("span", class_="name")

	# [*] add names to masterMatrix

	for chunk in nameChunks:
		name=chunk.get_text()
		print name
		masterMatrix.append(name)

#	print len(masterMatrix)

print len(masterMatrix)

# [*] create email address for each name

emails=[]
suffix="@<target>.com"

for candidate in masterMatrix:
	spaces=candidate.count(' ')
	if spaces < 2:
		first, last=candidate.split()
		fInitial=first[:1]
		finitialLower=fInitial.lower()
		lastLower=last.lower()
		emailAddress=finitialLower+lastLower+suffix
		print emailAddress
		emails.append(emailAddress)
	else:
		pass
print len(emails)
