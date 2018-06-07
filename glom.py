#!/usr/bin/python
#glom.py

############################################################
#                                                          #
#    [*] 2018.05.23                                        #
#          V0001                                           #
#          Black Lantern Security (BLS)                    #
#          @pjhartlieb                                     #
#                                                          #
#                                                          #
############################################################

import random
import re
from colorama import Fore
import csv

def readData(data):
    """
    Open gnmap file for operations

    Args
    ----------
    data (str): file passed

    Return
    -------
    data (list): Line by line list for the log file entries
    """
    with open(data, 'rb') as f:
        reader = csv.reader(f)
        dataEntries = list(reader)
    return dataEntries

def writetoFile(streams):
    """
    Write results to file

    Args
    ----------
    streams (list): host with open ports
    """
    thefile = open('snipeITimport.csv', 'w')
    for item in streams:
        thefile.write("%s\n" % item)

goWitness_entries= readData('goWitness_clean_ii.csv')
massDNS_entries= readData('resolved.csv')
nmap_entries= readData('nmap_clean.csv')
dnsNames_entries= readData('osint.csv')

print ""
print(
    Fore.BLUE + '[' + Fore.WHITE + '-' + Fore.BLUE + ']' + Fore.GREEN +
    str(len(dnsNames_entries)) + ' DNS names discovered')
print ""
print(
    Fore.BLUE + '[' + Fore.WHITE + '-' + Fore.BLUE + ']' + Fore.GREEN +
    str(len(massDNS_entries)) + ' IPs resolved to DNS names')
print ""
print(
    Fore.BLUE + '[' + Fore.WHITE + '-' + Fore.BLUE + ']' + Fore.GREEN +
    str(len(nmap_entries)) + ' hosts up with open ports')
print ""

snipeIT=[]

for i in dnsNames_entries:      # Select a resolved DNS name
    stream=[]                   # Initialize list to hold results
    stream.append(i[0])         # Append dns name to the list and set next 4 elements to null
    stream.append('null')       # [1]
    stream.append('null')       # [2]
    stream.append('null')       # [3]
    stream.append('null')       # [4]
    stream.append('null')       # [5]
    stream.append('null')       # [6]

    for j in massDNS_entries:   # Loop through resolved host names
        if i[0] == j[0] and stream[1] == 'null': # if match is found and nothing has been yet found for this
                                                 # entry, add IP tp stream and set next list element to null
                                                 # this is a place holder for the ports
            stream[1]=j[1]
            stream[2]='null'
        elif i[0] == j[0] and stream[1] != 'null': # if match is found and this host has already resolved to
                                                   # IP, add IP to stream (not clobbering the IP already there
                                                   # and set the next list element to null. This is the place
                                                   # holder for the ports.
            stream[3]=j[1]
            stream[4]='null'
    # end massDNS loop

    for k in nmap_entries:      # Loop through the nmap data
        if stream[1] == k[0]:   # If the IP for the nmap entry matches the first IP resolved to the DNS name
                                # then set the port placeholder @ stream[2] to the open ports
            stream[2]=(k[1:])
        elif stream[3] == k[0]: # If the IP for the nmap entry matches the second IP resolved to the DNS name
                                # then set the port placeholder @ stream[4] to the open ports
            stream[4]=(k[1:])
    # end nmap loop

    for r in goWitness_entries: # Loop through goWitness data
        if stream[0] == r[0]:   # If the dns name matches the goWitness entry
                                # enter the application and system/server data into the stream matrix
            stream[5] = r[2]
            stream[6] = r[3]
    # end goWitness loop

    snipeIT.append(stream)

#for result in snipeIT:
#    print result
#print len(snipeIT)

writetoFile(snipeIT)