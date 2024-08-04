#!/bin/bash
mkdir -p music_mnt
go-mtpfs music_mnt/ &
sleep 2
#for i in `/bin/ls -p /home/gareth/sideplay/songs/`
#do
#    echo "$i"
#done

for f in `/bin/ls -p "./music_mnt/Internal shared storage/Download/"`
do
    echo "$f"
done

fusermount -u music_mnt/