import time
import random
import datetime
import requests
import json
from random import randrange
import io
import string
import re
from wordnik import *
from bs4 import BeautifulSoup
import urllib2

definition=""
def1=""
example =""

def main():
    global definition    
    global def1
    global example
    #get random word from our wordlist
    search = open('/home/pi/wordlist.txt').read().splitlines()
    word = random.choice(search)
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    print timestamp
    print "Our random word is: " + word
    time.sleep(5)
    
    #get definition of word
    error = 0
    while error == 0:
        try:    
            url="https://kids.wordsmyth.net/we/?ent=" + str(word)
            opener = urllib2.build_opener()
            ourUrl = opener.open(url).read()
            soup = BeautifulSoup(ourUrl,"html5lib")
            definition = soup.find('tr',{'class': 'definition'})
            opener.close()
            if soup.find('tr',{'class': 'definition'}):
                definition = soup.find('tr',{'class': 'definition'})

                if definition.find('div',{'class': 'spanish'}).previousSibling:
                    def1 = definition.find('div',{'class': 'spanish'}).previousSibling
                    print "Definition: " + str(def1)

                if definition.find('em'):
                    example = definition.find('em').text
                    print "Example: " + str(example)
                else:
                    example = "Could not find example"
                    print "Could not find example"
            error = 1
        except Exception as e:
            print "Error, try again in 5 sec"
            time.sleep(5)
            pass
main()