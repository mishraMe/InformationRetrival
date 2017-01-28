import urllib
import HTMLParser
import nltk
from bs4 import BeautifulSoup as bs
import time
#variables and their initialization

pageCollectionLimit = 1000
sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
depthLimit = 3
currentLevel = 1
pagesAtCurrentDepth = [seedUrl]
pagesAtNextDepth = []
crawledPages = []
toBeCrawledPages = []
pg_no = 0
#the below function is used to extract raw html of the page to be saved

def extract_html_page(url, page_number):
    time.sleep(sleep_time)
    page = urllib.urlopen(url).read()
    file = open("D:/work/IR/assignment01/page_" + str(page_number) + ".txt", "w+")
    file.writelines("url : " + str(url) + '\n' + page)
    file.close()
    return page


def extract_new_links(page):
    soup = bs(page, 'html.parser')
    for tag in soup.find_all('a'):
        href = tag.get("href")
        if href is not None and ":" not in href and "#" not in href and "/wiki" in href:
            final_url = prefix + href
            pagesAtNextDepth.append(final_url)

    return pagesAtNextDepth


def inc():
    global pg_no
    pg_no += 1
    return pg_no

def updateLevel(new_depth_links):
    global currentLevel
    global pagesAtCurrentDepth
    currentLevel += 1
    pagesAtCurrentDepth = new_depth_links
    return


def crawlPagesInToBeCrawled(list_of_pages):
   temp = []
   for url in list_of_pages:
       pg_no = inc()
       page = extract_html_page(url, pg_no)
       temp = extract_new_links(page)
       toBeCrawledPages.remove(url)
       crawledPages.append(url)
   return temp


def startCrawling():
    while currentLevel <= depthLimit:
        print "current level is " + str(currentLevel)
        if crawledPages.__sizeof__() <= pageCollectionLimit:
            print "crawledPages size is " + str(crawledPages.__sizeof__())
            for url in pagesAtCurrentDepth:
                print "url is " + url
                pagesAtCurrentDepth.remove(url)
                if url not in crawledPages:
                    toBeCrawledPages.append(url)

        new_depth_links = crawlPagesInToBeCrawled(toBeCrawledPages)
        updateLevel(new_depth_links)
    return


def main():
    startCrawling()
    return

main()