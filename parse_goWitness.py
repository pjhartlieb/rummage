#!/usr/bin/python
#parse_goWitness.py

############################################################
#                                                          #
#    [*] 2018.05.17                                        #
#          V0002                                           #
#          Black Lantern Security (BLS)                    #
#          @pjhartlieb                                     #
#                                                          #
#                                                          #
############################################################

from bs4 import BeautifulSoup
import os
import codecs

"""

This utility will parse goWitness data. The input is "report.html". The output is a csv file.

The input file has been hard coded below.

[-] TBD
1. The input files should be command line arguments.

"""

if __name__ == '__main__':
    # Read in the target file
    # The second argument "lxml" specifies the parser
    soup = BeautifulSoup(open("report.html"), "lxml")

    # Capture the block of html for each target
    targets = soup.find_all("div", class_="card-block px-3")

    # Initialize target list
    targetList=[]

    # Loop through each target and parse data
    for element in targets:
        # Capture the target URL
        target_name = str(element.a.get_text())
        # Capture the response code
        response_code = str(element.small.get_text())
        # Capture the target technology
        poweredBy = element.find("td", text="X-Powered-By")
        if poweredBy:
            poweredbyValue = str(poweredBy.find_next_sibling("td").text.strip())
        else:
            poweredbyValue = "null"
        # Capture the target server
        server = element.find("td", text="Server")
        if server:
            serverValue = str(server.find_next_sibling("td").text.strip())
        else:
            serverValue = "null"
        # Create csv list
        value=target_name, response_code, poweredbyValue, serverValue
        targetList.append(value)

    # Initialize containers
    two_hundred=[]
    redirects=[]
    four_hundred=[]
    four_zero_three=[]
    four_zero_one=[]
    four_zero_four=[]

    # Sort responses
    for i in targetList:
        if i[1]=='200 OK':
            two_hundred.append(i)
        elif i[1]=='403 Forbidden':
            four_zero_three.append(i)
        elif i[1]=='401 Unauthorized':
            four_zero_one.append(i)
        elif i[1] == '404 Not Found':
            four_zero_four.append(i)
        elif i[1] == '400 Bad Request':
            four_hundred.append(i)

    # Metrics
    a=len(two_hundred)
    b=len(four_zero_three)
    c=len(four_zero_one)
    d=len(four_zero_four)
    e=len(four_hundred)
    f=a+b+c+d+e

    # Output
    print ""
    print "========== goWitness metrics =========="
    print ""
    print '\t[-] ' + str(a) + ' hosts are UP and DISPLAYING a web page (200)'
    print '\t[-] ' + str(b) + ' hosts FORBIDDEN (403)'
    print '\t[-] ' + str(c) + ' hosts UNAUTHORIZED (401)'
    print '\t[-] ' + str(d) + ' pages NOT FOUND (404)'
    print '\t[-] ' + str(e) + ' BAD REQUESTS (400)'
    print ""
    print '[-] ' + str(f) + ' TOTAL RESOURCES'

    # Write results to file
    resultsFile = open('outputFile.csv', 'a')

    for i in targetList:
        resultsFile.write(str(i)+'\n')
