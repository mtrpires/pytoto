# pytoto
A simple Python (2.7) scraper for the [Batoto Online Manga Reader](http://bato.to/)

This scraper uses Selenium, please refer to the [official documentation](http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html) to see how to install the Python bindings on your system. It shouldn't be more complex than:

`pip install selenium`

# Quickstart

Download script files to any folder and run from command line:

`python pytoto.py HASH ADBLOCK_FILE`

The hash of the manga is found when you’re browsing at Bato.to. You should use characters after the #. You can also provide a Chrome Extension file (CRX) of your favourite adblock extension. This is optional, but will considerably improve page load speeds, e.g.:

`python pytoto.py 13e499ca7e9c2c4a "AdBlock_v2.45.crx"`

### Important

You have to create an account at Bato.to and login in order to find the manga pages where the hashes are. The scraper doesn’t need to login.

# _functions.py

This file provides a list of functions and helper functions used in the scraping procedure. It has the following structure:

## Browsing functions

* `brInit()`: initialises the Chrome/Selenium webdriver.

* `urlLoad()`: loads URL with provided hash to webdriver.

* `imgGetURL()`: retrieves the URL that points to the image file of the current page.

## Manga functions

* `mgCrtFldr()`: Creates the series folder.

* `mgGetTtl()`: gets series title from HTML.

## Chapter functions

* `chChg()`: Uses Selenium’s dropdown capabilities to change chapter.

* `chGetInfo()`: Uses Selenium’s Select object to get the list of chapters from the dropdown menu.

* `chGetLen()`: Simply returns the length of the chapter list.

## Page functions

* `pgChg()`: Uses Selenium’s dropdown capabilities do change page.

* `pgGetList()`: Uses Selenium’s Select object to get the list of pages from the dropdown menu.

* `pgGetLen()`: Simply returns the lenght of the page list.

* `pgInfo()`: Retrieves the name of the page.

* `pgSave()`: Saves the image file locally.

# pytoto.py

This is the scraper robot. It initiates the Selenium Webdriver and is simply structured with two chained loops. The first iterates through the chapters list. The second iterates through the pages inside each chapter.

# todo

* Improve error handling (file/folder creation, network errors etc)

* Improve folder/file name adaptation (create cases for special characters like ":")

* Support for pause/resume

* Improve terminal output (refresh terminal and print info on the same line)


