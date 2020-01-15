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
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

definition=""
def1=""
example =""

def main():
    global definition    
    global def1
    global example
    #get random word from our wordlist
    search = open('wordlist.txt').read().splitlines()
    word = random.choice(search)
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    print timestamp
    print "Our random word is: " + word
    #must sleep for 90 seconds to get wifi after reboot
    print "Sleeping for 10 seconds while we wait for a network connection..."
    time.sleep(10)
    
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
        print "Writing HTML..."
        #generate html using the word and definition variables
        #Define HTML Template
        contents = '''<!DOCTYPE HTML>
<html>
    <head>
        <title>Word of the Day</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <!--[if lte IE 8]><script src="assets/js/html5shiv.js"></script><![endif]-->
        <link rel="stylesheet" href="assets/css/main.css" />
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.13/css/all.css" integrity="sha384-DNOHZ68U8hZfKXOrtjWvjxusGo9WQnrNx2sqG0tfsghAvtVlRW3tvkXWZh58N9jp" crossorigin="anonymous">

        <!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
        <!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
        <noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
        <link href="https://fonts.googleapis.com/css?family=Carter+One|Cinzel+Decorative|Montserrat:500|Open+Sans:600|Raleway:700" rel="stylesheet">
        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script>
        $(document).ready(function(){
        var header = $('body');

        var backgrounds = new Array(
            'url(images/w1.jpg)'
          , 'url(images/w2.jpg)'
          , 'url(images/w3.jpg)'
          , 'url(images/w4.jpg)'
          , 'url(images/w5.jpg)'
          , 'url(images/w6.jpg)'
          , 'url(images/w7.jpg)'
          , 'url(images/w8.jpg)'
        );

        var current = 0;

        function nextBackground() {
            current++;
            current = current %% backgrounds.length;
            header.css('background-image', backgrounds[current]);
        }
        setInterval(nextBackground, 300000);

        header.css('background-image', backgrounds[0]);
        });
        </script>
    </head>
    <body class="is-loading"  scroll="no" style="overflow: hidden">

        <!-- Wrapper -->
            <div id="wrapper">

                <!-- Main -->
                    <section id="main">
                        <header>
                            <center>                          
                            <h1><p>Word of the Day</p></h1>
                            <h2>%s</h2>
                            <p>Definition&nbsp;&bull;&nbsp;%s</p>
                            <p>Example&nbsp;&bull;&nbsp;%s</p> 
                            </center>
                        </header>
                    </section> 
                <!-- Footer -->
                    <footer id="footer">
                        <ul class="copyright">
                            <li><!--&copy; 2019--></li>
                        </ul>
                    </footer>

            </div>
                    <!-- Scripts -->
            <!--[if lte IE 8]><script src="assets/js/respond.min.js"></script><![endif]-->
            <script>
                if ('addEventListener' in window) {
                    window.addEventListener('load', function() { document.body.className = document.body.className.replace(/\\bis-loading\\b/, ''); });
                    document.body.className += (navigator.userAgent.match(/(MSIE|rv:11\.0)/) ? ' is-ie' : '');
                }
            </script>
    </body>
</html>''' % (str(word),str(def1),str(example))
        u = unicode(contents, "utf-8" )
        browseLocal(u)
        print "HTML generated"

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='index.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import os.path
    strToFile(webpageText, filename)
    #webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac

main()
