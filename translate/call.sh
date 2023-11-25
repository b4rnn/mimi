#!/bin/bash
#!/usr/bin/env python3.8
#script to send notifications

# we export the necessary environment variables
# Google license file
export GOOGLE_APPLICATION_CREDENTIALS="/opt/test/My First Project-1ebe2550f325.json"
# Project name
export GCLOUD_PROJECT=eng-district-216918
# python encoding
export PYTHONIOENCODING=UTF-8
#list of variables at the input
EMAIL=$1
CALLERIDNUM=$2
CALLERIDNAME=$3
FILE=$4
SPEECH_2_TEXT=`python3.8 /opt/test/voice.py /var/lib/asterisk/sounds/$FILE.wav  | sed -e 's/.*transcript"://' -e 's/}]}]}}//'`
JSON_TEXT=''$SPEECH_2_TEXT''
QUERY=$(jq -r '.text' <<< "$JSON_TEXT")
curl -H "Content-Type: application/json" -X POST -d '{"data":"'"$QUERY"'","tel":"'"$FILE"'"}' 127.0.0.1:5000/webhook

