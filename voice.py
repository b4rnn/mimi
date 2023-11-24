"""Google Cloud Speech API sample application using the REST API for batch
processing."""
import os
#import openai
import argparse
import base64
import json
import simplejson
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = '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'
#openai.api_key ='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'
client = OpenAI()

def main(speech_file):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    audio_file= open(speech_file, "rb")
    transcript = client.audio.transcriptions.create(
                 model="whisper-1", 
                 file=audio_file,
                 response_format='text'
	       )
   
    s = simplejson.dumps({"text":transcript}, ensure_ascii=False)
    print(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='Full path of audio file to be recognized')
    args = parser.parse_args()
    main(args.speech_file)

