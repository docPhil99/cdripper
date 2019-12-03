#!/bin/bash
LOCKDIR=/var/lock/cd_at_boot


function cleanup {
    echo "Cleaning up at $(date)"
}

trap "cleanup" EXIT
echo "starting cd_boot.sh"
if [[ "$1" == "--clear" ]]; then
    echo "Removing lock dir: $LOCKDIR"
    if [ -d $LOCKDIR ]; then
        if rmdir $LOCKDIR; then
            exit 0
        else
            echo "Error failed to remove $LOCKDIR"
            exit -1
        fi
    else
        echo "$LOCKDIR does not exist"
        exit 0
    fi
elif [[ "$1" == "--status" ]]; then
    if [ -d  $LOCKDIR ]; then
        echo "Lock exists"
        exit 1
    else
        echo "$LOCKDIR does not exist"
        exit 2
    fi
elif [[ "$1" != "--probe" ]]; then
    echo "Error, expecting either: --clear, --status, or --probe"
    exit -1
fi

val="$(/home/phil/dev/cdinfo/cdinfo /dev/sr0)"
res=$?
echo "cdinfo output: $val"
echo "exit status: $res"
if [ $res -eq 4 ]; then
    echo "Disc detected"
    if mkdir -p $LOCKDIR; then
        echo "created lock at $LOCKDIR"
    else
        echo "Cannot create lock dir: $LOCKDIR"
        exit -1
    fi
fi
