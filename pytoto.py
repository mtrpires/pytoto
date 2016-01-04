# -*- coding: utf-8
# Pytoto Manga Downloader
# A simple Python scraper for the Batoto Online Manga Reader.
#
# Bato.to - http://bato.to/
#
# This scraper uses Selenium (Chrome), please refer to:
# http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html
#
# This code is 75 columns wide for clarity.
# Names of functions with multiple words are spaced by capitalisation.
# Names of variables with multiple words are spaced by underscore.
#
# Usage: pytoto.py HASH "adblocker.crx" (optional)
# HASH: Hash of wanted manga found in the url. Characters after #
# from http://bato.to/reader#13e499ca7e9c2c4a
#
# e.g. python pytoto.py 13e499ca7e9c2c4a "AdBlock_v2.45.crx"
#
# Optional: Pytoto also allows you to use an adblock extension. Use the
# filepath to the crx file as a second parameter.
#
# @mtrpires
#
from sys import argv
from time import sleep
from time import time
from random import uniform
from _functions import brInit
from _functions import urlLoad
from _functions import imgGetURL
from _functions import mgCrtFldr
from _functions import mgGetTtl
from _functions import chChg
from _functions import chGetInfo
from _functions import chGetLen
from _functions import pgChg
from _functions import pgGetList
from _functions import pgGetLen
from _functions import pgInfo
from _functions import pgSave

#start counter
start_time = time()

#Go to Manga root page
URL = "http://bato.to/reader#{0}".format(argv[1])
adb = argv[2]
driver = brInit(adb_crx = adb)
urlLoad(driver, URL)

#Get Manga information & create folder
title = mgGetTtl(driver)
mgCrtFldr(title)

#Find chapters, create a dict and store its length
chapter_dict = chGetInfo(driver)
chapter_total = len(list(chapter_dict))
chapter_len = chapter_total
print "Found", chapter_len, "chapters."

#iterates through the chapters
for key in chapter_dict:
    volume_and_chapter = chChg(driver, key)
    #Waits between 3-5 seconds for page to load
    #Some JS may take longer to show up.
    #Also, I don't want to flood the server with requests.
    rd_sleep = uniform(3, 5)
    sleep(rd_sleep)
    volume = volume_and_chapter[0]
    chapter = volume_and_chapter[1]
    #this is to calculate progress...
    chapter_len -= 1
    #gets the number of pages.
    page_select = pgGetList(driver)
    page_len = pgGetLen(page_select)
    print "Found", page_len, "pages in", volume, chapter
    #iterates through the pages
    for page in range(page_len):
        # A naughty workaround for webpages that load faster than
        # Selenium is able to update and get the pages list.
        # Usually pages load just fine, but sometimes Selenium needs a 
        # second try to get it right.
        flag = True
        while flag:
            try:
                page_select = pgGetList(driver)
                pgChg(page_select, page)
                flag = False
            except:
                print "Error retrieving chapter information. Trying again."
        rd_sleep = uniform(3, 5)
        sleep(rd_sleep)
        flag = True
        while flag:
            try:
                img_url = imgGetURL(driver)
                print "URL:", img_url
                flag = False
            except:
                print "Error retrieving img URL. Trying again."
        #updates driver object with current HTML
        page_select = pgGetList(driver)
        page_info = pgInfo(page_select)
        pgSave(img_url, title, volume, chapter, page_info)
        percent = 100-(chapter_len/chapter_total)
    print ">>> {0} completed".format(percent)

time_minutes = (time()-start_time)/60

print "Finished downloading", title
print("--- {0:.2f} minutes ---".format(time_minutes))
print
