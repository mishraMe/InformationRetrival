import urllib2
from bs4 import BeautifulSoup as bs
import time
#variables and their initialization

pageCollectionLimit = 1000
sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
mainPage = "/wiki/Main_Page"
sustainableEnergyLinks = "D:/work/IR/assignment02/sustainableEnergyLinks.txt"
depthLimit = 2
currentLevel = 1
crawledPages = []
toBeCrawledPages = []
pg_no = 0
#the below function is used to extract raw html of the page to be saved

def extract_html_page(full_url, page_number):
    time.sleep(sleep_time)
    page = urllib2.urlopen(full_url).read()
    file = open("D:/work/IR/assignment02/page_" + str(page_number) + ".txt", "w+")
    file.writelines("url : " + str(full_url) + '\n' + page)
    file.close()
    return page

def extract_new_links(page):
    soup = bs(page, 'html.parser')
    for tag in soup.find_all('a'):
        href = tag.get("href")
        if href is not None and "/wiki/" in href:
            if ":" in href or "#" in href or "." in href or "?" in href or href == mainPage:
                continue
            else:
                final_url = prefix + href
                toBeCrawledPages.append(final_url)
    return



def inc():
    global pg_no
    pg_no += 1
    return pg_no

def updateLevel():
    global currentLevel
    currentLevel += 1
    print currentLevel
    return

# we always check the updated crawled list and then fill the toBeCrawledPages list
#thus it will always have only one url in its list to crawl
def crawlPagesInToBeCrawled(urls):
   for url in urls:
       if len(crawledPages) < pageCollectionLimit:
           if url in crawledPages or check_redirected_url(url) in crawledPages:
               toBeCrawledPages.remove(url)
               continue
           else:
               pg_no = inc()
               page = extract_html_page(url, pg_no)
               extract_new_links(page)
               crawledPages.append(url)
               toBeCrawledPages.remove(url)
       else:
         return -1
   updateLevel()
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
        temp = []
        for element in toBeCrawledPages:
            temp.append(element)
        crawled_limit = crawlPagesInToBeCrawled(temp)
        if crawled_limit == -1:
            return
    print "current level is greater than the level limit"
    return

def crawlSeed():
    toBeCrawledPages.append(seedUrl)
    startCrawling()
    listPagesCrawled(crawledPages)
def main():
    crawlSeed()

main()