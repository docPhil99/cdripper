#!/bin/bash
LOCKDIR=/var/lock/rip.lock
LOGFILE=/home/phil/dev/log.txt
#rm $LOGFILE
function cleanup {
 if rmdir $LOCKDIR; then
	echo "Finished $(date)" >> $LOGFILE
        #rm $LOGFILE
        popd
 else
	echo "Failed to remove lock dir '$LOCKDIR'" >> $LOGFILE
        popd
      	exit 1
 fi
}
if mkdir $LOCKDIR; then
	trap "cleanup" EXIT
	echo "Acquired Lock, running" >> $LOGFILE
	echo "Started $(date) $$" >> $LOGFILE

        pushd  "$(dirname "$0")"
        echo "Setting cwd to $(pwd)" >> $LOGFILE
        val="$(/home/phil/dev/cd_boot.sh --status)"
        res=$?
        echo "cd_at_boot: $val" >> $LOGFILE
        echo "res=$res" >> $LOGFILE
        if [ $res -eq 1 ]; then
            echo "Boot lock detected, not running" >> $LOGFILE
            echo "Clearing lock" >> $LOGFILE
            val="$(/home/phil/dev/cd_boot.sh --clear)"
            res=$?
            echo "$val" >> $LOGFILE
            exit 0
        fi
        n=0
        while [ $n -le 3 ]; do
            val="$(cdinfo/cdinfo /dev/sr0)"
            res=$?
            echo "try: $n" >> $LOGFILE
            echo "cdinfo output: $val" >> $LOGFILE
            if [ $res -ne -1 ]; then
                break
            fi
            let i = i + 1
            sleep 4
        done
        if [ $res -eq 4 ]; then
	    abcde -c /home/phil/dev/abcde.conf >>$LOGFILE 2>&1
            #trigger LMS rescan
            echo "Rescan library $(date) $$" >> $LOGFILE
            wget -q --spider http://localhost:9000/settings/index.html?p0=rescan
            echo "Done $(date)" >> $LOGFILE
            echo "Set backup flag to run">>$LOGFILE
            /home/phil/dev/set_backup_flag.sh
            cat $LOGFILE | mail -s "Ripper log" dr.phil.birch@gmail.com
            #eject
            echo "Sending webhook:">>$LOGFILE
            /home/phil/dev/ifttt_send.sh "Ripper done. Please eject CD" >> $LOGFILE
            #rm $LOGFILE
        else
            echo "Disc error, not running abcde $(date) $val  $res" >> $LOGFILE
        fi    
	echo "Stopped $(date) $$" >> $LOGFILE
        savelog -l -c 5 $LOGFILE
        #popd
else
	echo "Could not create lock, already running? '$LOCKDIR'" 
        exit 1
fi
