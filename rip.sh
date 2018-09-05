#!/bin/bash
LOCKDIR=rip.lock
LOGFILE=/home/phil/dev/log.txt
rm $LOGFILE
function cleanup {
 if rmdir $LOCKDIR; then
	echo "Finished $(date)" >> $LOGFILE
        #rm $LOGFILE
 else
	echo "Failed to remove lock dir '$LOCKDIR'" >> $LOGFILE
      	exit 1
 fi
}
if mkdir $LOCKDIR; then
	trap "cleanup" EXIT
	echo "Acquired Lock, running" >> $LOGFILE
	echo "Started $(date) $$" >> $LOGFILE
        val=$(cdinfo/cdinfo /dev/sr0)
        res=$?
        if [ $res -eq 4 ]; then
	    abcde -c /home/phil/.abcde.conf >>$LOGFILE 2>&1
            #trigger LMS rescan
            echo "Rescan library $(date) $$" >> $LOGFILE
            wget -q --spider http://localhost:9000/settings/index.html?p0=rescan
            echo "Done $(date)" >> $LOGFILE
            cat $LOGFILE | mail -s "Ripper log" dr.phil.birch@gmail.com
        else
            echo "Disc error, not running abcde $(date) $val" >> $LOGFILE
        fi    
	echo "Stopped $(date) $$" >> $LOGFILE
else
	echo "Could not create lock, already running? '$LOCKDIR'" 
        exit 1
fi
