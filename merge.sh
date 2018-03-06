#!/bin/bash

#provide target directory
dir="$1"
dirb="$1/*"

for f in $dirb
do
  fullfilename=$(basename "$f")
  extension="${fullfilename##*.}"
  name="${fullfilename%%.*}"
  directoryName=$(dirname "$f")

  if [ -f "$f" ] && [ "$extension" == 'tar' ]; then
     #mkdir $directoryName\/$name
     #echo $directoryName\/$name
     #echo "$name"
     tar -xf  $f -C $directoryName
     tarb="$directoryName/psoftcaps/*"

     for g in $tarb
     do
       fullgzfilename=$(basename "$g")
       gzextension="${fullgzfilename##*.}"
       gzname="${fullgzfilename%%.*}"
       gzdirectoryName=$(dirname "$g")
#       echo $g
       if [ -f "$g" ] && [ "$gzextension" == 'gz' ]; then
#          echo $fullgzfilename
#          echo $gzextension
          gunzip $g
       else
         :
       fi
     done
     mergecap $tarb.pcap -w <date>_merged.pcap
  else
    :
  fi
done
