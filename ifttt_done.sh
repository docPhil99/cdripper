#!/bin/bash
source /home/phil/dev/ifttt_key.sh
curl -H "Content-Type: application/json" -X POST -d '{}'  https://maker.ifttt.com/trigger/ripper_done/with/key/$IFTTT_KEY
