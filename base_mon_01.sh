#!/bin/bash

#   network baseline monitoring
#   written by pjhartlieb
#   2011.12.09
#   Mac OSX 10.6.8
#   version 0.1

#create timestamps
stamp=`date +%y%m%d`
stmp_1=`date -v -1d +%y%m%d`
stmp_2=`date -v -2d +%y%m%d`

#create formatting variables
format='%-8s %-15s %-6s %-6s %-6s %-6s %-6s %-6s %-6s' #format process output
lformat='%-15s %-15s %-15s %-15s' #format listener output

#create log directories
for i in /var/log/reports/network /var/log/basemon; do
   if [ -d "$i" ]; then
     :
     else
     echo ""
     echo "creating $i directory ..."
     mkdir -p $i
   fi
done

#identify the listening ports on the system
##write the ports to a file > /tmp/listening_ports
netstat -an|grep -i list|awk '{print $4}'|egrep -o \.[0-9]\{1,\}$|sed 's/\.//g'|sort -u > /tmp/listening_ports

##identify all processes that are using network resources
lsof -i -t > /tmp/network_usage_pids
### set variables
      n_pids="/tmp/network_usage_pids"
      IFS=$'\n' #handles echo processing embedded in loops

##dump the currently running processes to a file
ps -efc > /tmp/$stamp"_ps_dump"
ps_dump=/tmp/$stamp"_ps_dump"

##parse and display data for each process 
### the w/i comparison lets me pluck items from ps output for the report    
    echo " "
    echo "the following PIDs are consuming NETWORK RESOURCES .... "
    echo ""
    printf "${format}\n" "PID" "comm" "UID" "PPID" "OBS" "files" "curr" "prev" "common"
	for i in `cat $n_pids`; do
         for q in `cat $ps_dump`; do
          w=`echo $q|awk '{print $2}'`
           if [ "$w" == "$i" ]; then
	    #PPID and UID
              uid=`echo $q|awk '{print $1}'`
	      ppid=`echo $q|awk '{print $3}'`
	    #command used
	      cmd=`echo $q|grep $i|awk '{print $8}'` 
	    #accessed files
	      lsof -p $i|awk '{print $9}'|sort -u|sed '/^$/d' > /var/log/basemon/$cmd"_network_files_"$stamp
            #accessed file count
              ctn=`cat /var/log/basemon/$cmd"_network_files_"$stamp|wc -l`
	      ct=`echo $ctn|sed 's/ //g'` 
            #compare files accessed with the previous days record
	      today="/var/log/basemon/$cmd"_network_files_"$stamp"
	      yesterday="/var/log/basemon/$cmd"_network_files_"$stmp_1"
	       if [ -e $yesterday ]; then
	          unq_todayn=`comm -13 $yesterday $today|wc -l`
		  unq_today=`echo $unq_todayn|sed 's/ //g'` 
		  unq_yesterdayn=`comm -23 $yesterday $today|wc -l`
		  unq_yesterday=`echo $unq_yesterdayn|sed 's/ //g'` 
		  commonn=`comm -12 $yesterday $today|wc -l`
		  common=`echo $commonn|sed 's/ //g'` 
		  ct=`echo $ctn|sed 's/ //g'` 
		  obs="Y"
    	          printf "${format}\n" $i $cmd $uid $ppid $obs $ct $unq_today $unq_yesterday $common
   	       else
		  obs="N"
    	          printf "${format}\n" $i $cmd $uid $ppid $obs $ct x x x
	       fi
             else
             #do nothing
             :
             fi
        done
done

## parse and display data for active listeners
    echo " "
    echo "the following PIDs have ACTIVE LISTENERS .... "
        echo " "
    	printf "${lformat}\n" PID port comm user
	for i in `cat /tmp/listening_ports`; do
		#PID
		  lpid=`lsof -i :$i|grep LISTEN|awk '{print $2}'|sort -u`
		#command
		  lcomm=`lsof -i :$i|grep LISTEN|awk '{print $1}'|sort -u`
		#user
		  luser=`lsof -i :$i|grep LISTEN|awk '{print $3}'|sort -u`
    		printf "${lformat}\n" $lpid $i $lcomm $luser
	done	 

## parse and display data for established sessions
    echo " "
    echo "the following PIDs have ESTABLISHED SESSIONS  .... "
        echo " "
    	printf "${lformat}\n" PID comm user
	for q in `cat $n_pids`; do
		 established=`lsof -p $q|grep ESTABLISHED`
		 if [ `echo $established|wc -m` -gt 1  ]; then
		#command
		  lcomm=`echo $established|awk '{print $1}'|sort -u`
		#user
		  luser=`echo $established|awk '{print $3}'|sort -u`
    		printf "${lformat}\n" $q $lcomm $luser
		 else
		   :
		fi
	done

# cleanup
rm -f /tmp/listening_ports
rm -f $n_pids
rm -f $ps_dump
rm -f /var/log/basemon/*_network_files_$stmp_2

#sort out FD and those that need to be counted
#look at established sessions as well
