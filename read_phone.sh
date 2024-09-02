#!/bin/bash

IFS=$'\n'
for f in `/bin/ls -b -p /home/gareth/sadguriplay/music_mnt/Internal\ shared\ storage/Download`
do
	echo "$f"
done
