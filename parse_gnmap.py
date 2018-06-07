#!/usr/bin/python
#parse_gnmap.py

############################################################
#                                                          #
#    [*] 2018.05.22                                        #
#          V0001                                           #
#          Black Lantern Security (BLS)                    #
#          @pjhartlieb                                     #
#                                                          #
#                                                          #
############################################################

import random
import re
from colorama import Fore

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
    f=open(data, 'rb')
    dataEntries = f.read().splitlines()
    return dataEntries


def preProc(dataEntries):
    """
    Extract host and open ports

    Args
    ----------
    dataEntries (list): line by line entries for the gnmap file

    Return
    -------
    streams (list): select metadata for each gnmap result
    """
    streams = []

    print(
        Fore.BLUE + '[' + Fore.WHITE + '-' + Fore.BLUE + ']' + Fore.GREEN + ' Pre-processing ' +
                                            str(len(dataEntries)) + '  lines of nmap results')
    print ""

    for datum in dataEntries:
        stream=[]
        host_ports_match = re.search("Host: [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(.*)Ports", datum)
        if host_ports_match:
            blob=host_ports_match.group(0)
            host_match = re.search("Host: [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", blob)
            ports_match = re.search("Ports:(.*)", datum)
            if host_match:
                host = host_match.group(0)
                pair=host.split(':')
                host=pair[1].replace(" ","")
                stream.append(host)
            if ports_match:
                ports = ports_match.group(0)
                ports_final = re.findall("[0-9]{1,}\/[a-z0-9\-]{1,}\/[a-z0-9\-]{1,}\/\/[a-z0-9\-]{1,}\/\/\/", ports)
                for i in ports_final:
                    portf_match = re.match("[0-9]{1,}\/open",i)
                    if portf_match:
                        port_data = portf_match.group(0)
                        pair=port_data.split('/')
                        port = pair[0].replace(" ", "")
                        stream.append(port)
        if stream:
            streams.append(stream)

    return streams

def writetoFile(streams):
    """
    Write results to file

    Args
    ----------
    streams (list): host with open ports
    """
    thefile = open('nmap_results.csv', 'w')
    for item in streams:
        thefile.write("%s\n" % item)

dataEntries = readData('nmap.gnmap')
streams = preProc(dataEntries)
writetoFile(streams)