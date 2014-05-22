#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from optparse import OptionParser
import subprocess

BASE_URL="http://translate.google.com/translate_tts?tl=pt&q="
FILE_PREFIX="audio_"
FILE_SUFFIX=".mp3"
FILE_COUNT=0
AUDIO_FILES=[]

def parse_phrase(phrase):
   temp = phrase.split(" ")
   result = []
   out = ""
   
   for text in temp:
      if ( (len(out) + len(text)) < 99 ):
         out = out + " " + text
      else:
         result.extend([out])
         out = text
   result.extend([out])
   return result

def tts(text_tokens):
   global FILE_COUNT
   global AUDIO_FILES

   for token in text_tokens:
      URL = BASE_URL + remove_space(token)
      command = ["curl",URL,"--user-agent","\"Mozilla/5.0\"","-o",FILE_PREFIX+str(FILE_COUNT)+FILE_SUFFIX]
      subprocess.call(command)
      AUDIO_FILES.extend([FILE_PREFIX+str(FILE_COUNT)+FILE_SUFFIX])
      FILE_COUNT += 1

def remove_space(text):
   return text.replace(" ", "%20")

def main():

   global FILE_COUNT

   parser = OptionParser()
   parser.add_option("-f", "--file", dest="text_file",
                  help="Read file from text file", metavar="text_file")

   (options, args) = parser.parse_args()

   with open(options.text_file) as f:
      content = f.readlines()

   for text in content:
      tts(parse_phrase(text))

   command = ["/usr/bin/mplayer","-ao","alsa","-really-quiet","-noconsolecontrols"]
   command.extend(AUDIO_FILES)
   #print command
   subprocess.call(command)


if __name__ == '__main__':
   main()


