#!/bin/bash
source /home/phil/dev/ifttt_key.sh
echo $IFTTT_KEY
echo $1
CMDSTRING=("curl -H \"Content-Type: application/json\" -X POST -d '{\"value1\":\" $1\"}'  https://maker.ifttt.com/trigger/ripper_done/with/key/$IFTTT_KEY")
echo $CMDSTRING
eval $CMDSTRING
