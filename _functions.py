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
# filepath to the crx file as a second parameter. If you don't use an
# adblocker, pages may take forever to load.
#
# @mtrpires
#

import os
import urllib2
from time import sleep
from random import uniform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

#Browser functions
def brInit(adb_crx=None):
    """
    Initialises Selenium's webdriver (Chrome)
    This version uses an adblock extension to load pages faster.
    Download the crx file and save it in the same folder.
    You can use any extension you want.

    return: webdriver object
    """
    if adb_crx == None:
        driver = driver = webdriver.Chrome()
    else:
        chop = webdriver.ChromeOptions()
        chop.add_extension(adb_crx)
        driver = webdriver.Chrome(chrome_options = chop)
    return driver

def urlLoad(webdriver, url):
    """
    Loads the page using the webdriver with a given URL
    webdriver: Selenium's webdriver object
    url: string

    return: it updates the webdriver and prints confirmation.
    """
    webdriver.get(url)
    print "Page loaded successfuly."

def imgGetURL(webdriver):
    """
    Gets IMG url for download
    webdriver: Selenium's webdriver

    return: string with URL
    """
    element = webdriver.find_element_by_id("comic_page")
    url = element.get_attribute("src")
    return url

#Manga functions
def mgGetTtl(webdriver):
    """
    Gets Manga title
    webdriver: Selenium's webdriver object
    
    return: unicode string with title
    """
    title = webdriver.title
    title = title.split(" - ")[0]
    return title

def mgCrtFldr(manga_title):
    """
    Creates the root folder for the series using the Manga title.
    mangaTitle: unicode string from getMangaTitle()
    
    return: it prints confirmation the folder was created
    """
    if not os.path.exists(manga_title):
        os.makedirs(manga_title)
        print "Folder '{0}' created successfully.".format(manga_title)
    else:
        print "Folder '{0}' already exists. I won't replace it."\
            .format(manga_title)

def vlCrtFldr(title, volume):
    """
    Creates a folder for the respective Volume being downloaded.
    title: unicode string from getMangaTitle()
    volume: int from getMangaInfo(), index 0

    return: it prints confirmation the folder was created
    """
    manga_volume = "{0}/{1} - Vol.{2}".format(title, title, volume)
    if not os.path.exists(manga_volume):
        os.makedirs(manga_volume)
        print "Created:", manga_volume
    else: print "Folder '{0}' already exists. I won't replace it."\
        .format(manga_volume)


#Chapter functions
def chChg(webdriver, key):
    """
    Changes the chapter using the UI helper from the Select object
    webdriver: Selenium's webdriver
    value: key from generated dict from chGetInfo()

    return: list containing volume and chapter information.
    """
    select_object = chSelect(webdriver)
    select_object.select_by_visible_text(key)
    volume_and_chapter = key.split(" ", 1)
    print "Chapter changed."
    return volume_and_chapter

def chGetLen(webdriver):
    """
    Gets the length of the list of chapters.
    webdriver: Selenium's webdriver object

    return: int
    """
    select_object = chSelect(webdriver)
    chapter_list = select_object.options
    return len(chapter_list)

def chSelect(webdriver):
    """
    Generates a Select object from the chapter list found in any page.
    
    return: Selenium's Select object
    """
    chapter_list = webdriver.find_element_by_name("chapter_select")
    select_object = Select(chapter_list)
    return select_object

def chGetInfo(webdriver):
    """
    Gets the chapter list and transforms it into a dictionary.
    webdriver: Selenium's webdriver object

    return: dictionary 
    key: Volume and Chapter numbers
    Value: Link to corresponding chapter
    """
    select_object = chSelect(webdriver)
    chapter_dict = {}
    for item in select_object.options:
        chapter_dict[item.text] = item.get_attribute("value")
    return chapter_dict

#Page functions
def pgChg(select_object, index):
    """
    Changes the page using the UI helper from the Select object
    selectObject: Selenium's Select object from getPgList()
    index: int - the index corresponding to the getPgLen()

    return: it confirms the page was changed.
    """
    select_object.select_by_index(index)
    selected_page = select_object.first_selected_option
    print "Changed to", selected_page.text

def pgGetLen(select_object):
    """
    Gets the page list.
    selectObject: Selenium's Select object from getPgList()
    
    return: int
    """
    page_list = select_object.options
    return len(page_list)

def pgGetList(webdriver):
    """
    Gets the chapter list.
    webdriver: Selenium's webdriver object
    
    return: Select object
    """
    page_list = webdriver.find_element_by_name("page_select")
    return Select(page_list)

def pgInfo(select_object):
    """
    Gets page number.
    
    return: unicode string with page name/number.
    """
    selected_page = select_object.first_selected_option
    return selected_page.text

def pgSave(img_url, title, volume, chapter, page):
    """
    Saves current page locally.
    img_url: URL to page.
    title: unicode string from mgGetTtl()
    volume: int from chChg()
    chapter: int from ChChg()
    page: int from getMangaInfo()

    return: prints confirmation page was saved.
    """
    img = urllib2.urlopen(img_url).read()
    filename = os.path.abspath('{0}/{1} - {2}/{3} - {4} {5} - {6}.jpg'\
        .format(title, title, volume, title, volume, chapter, page))
    volume_folder = os.path.abspath('{0}/{1} - {2}'\
        .format(title, title, volume))
    if not os.path.exists(volume_folder):
        os.makedirs(volume_folder)
    if not os.path.exists(filename):
        with open(filename, 'w+') as pg_file:
            pg_file.write(img)
            pg_file.close()
            print page, "saved successfully."
    else:
        print "File '{0}' already exists! I won't replace it"\
        .format(filename)
