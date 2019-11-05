#!/bin/bash
#returns 0 if backup is set to run today, and clears the flag file
#return 1 if it not to run
if [ -f  "/home/phil/.run_backup_today" ]; then
    #echo "Backup flag exists, clearing"
    rm /home/phil/.run_backup_today
    exit 0
else
    #echo "Backup not marked to run"
    exit 1
fi

