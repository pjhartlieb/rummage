#!/usr/bin/python

############################################################
##
##		builder.py v0.0.1
##
##		Data processing for keepNote file
##
##		by pjhartlieb
##
############################################################

from BeautifulSoup import BeautifulSoup
import sys
import csv
import re
import os
import time

# Find all "page.html" files and write full file paths to a list
target_files=[]
for root, directories, filenames in os.walk('/path/to/directory'):
	for filename in filenames:
		fullName=os.path.join(root,filename)
		if re.match(r'.*page.html$',filename) and re.match(r'.*/adminstrative/.*|.*/technical/.*|.*/physical/.*',fullName):
			file_number=len(target_files)

			target_files.append(fullName)

# Iterate over each file in the list
# Extact fields
# Write Fields to a new list
# Write list to the csv file
for targetFile in target_files:
	# Initialize array
	fields=[]

	# Read in html file
	target=open(targetFile)

	# Create object for BeautifulSoup to operate on
	soup=BeautifulSoup(target)

	# HIPAA CFR requirement title
	if soup.title != "":
		title=soup.title.getText()
		title=title.encode('utf-8')
		fields.append(title)
	#print title

	# HIPAA CFR requirement type
	children=soup.body.getText()
	if re.search(r'\[(STANDARD|REQUIRED|ADDRESSABLE)\]',children):
		reType=re.search(r'\[(STANDARD|REQUIRED|ADDRESSABLE)\]',children)
		reType=re.sub('\[|\]','',reType.group())
		reType=reType.encode('utf-8')
		fields.append(reType)
	else:
		reType='N/A'
		fields.append(reType)

	# HIPAA CFR requirement description
	if re.search(r'\-.*?\?',children):
		reDesc=re.search(r'\-.*?\?',children)
		reDesc=re.sub('\- ','',reDesc.group())
		reDesc=reDesc.encode('utf-8')
		fields.append(reDesc)
	else:
		reDesc='N/A'
		fields.append(reDesc)

	# BLS products and artifacts
	if re.search(r'\[PRODUCTS\]\-.*?\[',children):
		redescProducts=re.search(r'\[PRODUCTS\]\-.*?\[',children)
		descProducts=re.sub('\[PRODUCTS\]\-', '',redescProducts.group())
		descProducts=re.sub('\[|^ |\-', '',descProducts)
		descProducts=descProducts.encode('utf-8')
		fields.append(descProducts)
	else:
		descProducts='N/A'
		fields.append(descProducts)

	# Append "fields" list to the csv file as a new row
	with open("output.csv", "a") as fp:
		wr=csv.writer(fp, dialect='excel')
		wr.writerow(fields)
	#for i in fields:
	#	print i

	del fields[:]
