#!/bin/bash
CALLERIDNUM=+254718192848--254208789522--24-11-2023--13-40-36
SPEECH_2_TEXT=`python3.8 /opt/test/voice.py /var/lib/asterisk/sounds/+254718192848--254208789522--24-11-2023--13-40-36.wav  | sed -e 's/.*transcript"://' -e 's/}]}]}}//'`
echo $SPEECH_2_TEXT
JSON_TEXT=''$SPEECH_2_TEXT''
QUERY=$(jq -r '.text' <<< "$JSON_TEXT")
curl -H "Content-Type: application/json" -X POST -d '{"data":"'"$QUERY"'","tel":"'"$CALLERIDNUM"'"}' 127.0.0.1:5000/webhook
