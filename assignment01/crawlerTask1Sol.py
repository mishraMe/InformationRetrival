import urllib2
import HTMLParser
import nltk
from bs4 import BeautifulSoup as bs
import time
#variables and their initialization

pageCollectionLimit = 1000

sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
mainPage = "/wiki/Main_Page"
sustainableEnergyLinks = "D:/work/IR/assignment01/sustainableEnergyLinks.txt"
depthLimit = 5
currentLevel = 1
pagesAtCurrentDepth = [seedUrl]
pagesAtNextDepth = []
crawledPages = []
toBeCrawledPages = []
pg_no = 0
#the below function is used to extract raw html of the page to be saved

def extract_html_page(full_url, page_number):
    time.sleep(sleep_time)
    page = urllib2.urlopen(full_url).read()
    file = open("D:/work/IR/assignment01/page_" + str(page_number) + ".txt", "w+")
    file.writelines("url : " + str(full_url) + '\n' + page)
    file.close()
    return page

def extract_new_links(page):
    soup = bs(page, 'html.parser')
    for tag in soup.find_all('a'):
        href =  tag.get("href")
        if href is not None and "/wiki/" in href:
            if ":" in href or "#" in href or "." in href or "?" in href or "=" in href or href == mainPage:
                continue
            else:
                final_url = prefix + href
                pagesAtNextDepth.append(final_url)
        else:
            continue
    return



def inc():
    global pg_no
    pg_no += 1
    return pg_no

def updateLevel(new_depth_links):
    global currentLevel
    global pagesAtCurrentDepth
    global pagesAtNextDepth
    currentLevel += 1
    pagesAtCurrentDepth = new_depth_links
    pagesAtNextDepth = []
    return


def crawlPagesInToBeCrawled(list_of_pages):
   for url in list_of_pages:
       if len(crawledPages) < pageCollectionLimit:
           pg_no = inc()
           page = extract_html_page(url, pg_no)
           extract_new_links(page)
           toBeCrawledPages.remove(url)
           crawledPages.append(url)
       else:
           return -1
   return

def listPagesCrawled(pages_crawled):
    file = open(sustainableEnergyLinks, "w+")
    for page in pages_crawled:
        file.writelines(page + '\n')
    file.close()
    return

def check_redirected_url(full_url):
    redirect_handler = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = redirect_handler.open(full_url)
    final_url = request.url
    #print "final value of redirected url is " + final_url
    return final_url

def startCrawling():
    while currentLevel <= depthLimit:
        for url in pagesAtCurrentDepth:
            pagesAtCurrentDepth.remove(url)
            url = check_redirected_url(url)
            if url not in crawledPages:
                toBeCrawledPages.append(url)
                crawled_limit = crawlPagesInToBeCrawled(toBeCrawledPages)
                if crawled_limit:
                    return crawledPages
        new_depth_links = pagesAtNextDepth
        updateLevel(new_depth_links)
    print "current level is greater than the level limit"
    return crawledPages


def main():
    pagesCrawled = startCrawling()
    listPagesCrawled(pagesCrawled)


main()