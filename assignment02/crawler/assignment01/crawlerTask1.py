import urllib2
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import time
import sys
#variables and their initialization
# the final program for task1
pageCollectionLimit = 1000
sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
mainPage = "/wiki/Main_Page"
sustainableEnergyLinks = "task_1_links_final.txt"
directory_name = "task_1_docs_final"
depthLimit = 5
currentLevel = 1
crawledPages = []
toBeCrawledPages = []
graph = OrderedDict()
pg_no = 0
#the below function is used to extract raw html of the page to be saved

def extract_html_page(full_url, page_number):
    time.sleep(sleep_time)
    page = urllib2.urlopen(full_url).read()
    # file = open(directory_name + "/page_" + str(page_number) + ".txt", "w+")
    # file.writelines("url : " + str(full_url) + '\n' + page)
    # file.close()
    return page

def extract_new_links(page):
    outlinks = []
    soup = bs(page, 'html.parser')
    for tag in soup.find_all('a'):
        href = tag.get("href")
        if href is not None and "/wiki/" in href:
            if ":" in href or "#" in href or "." in href or "?" in href or href == mainPage:
                continue
            else:
                final_url = prefix + href
                toBeCrawledPages.append(final_url)
                outlinks.append(final_url)
    return outlinks



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
   global graph
   outlinks_of_page = []
   for url in urls:
       if len(crawledPages) < pageCollectionLimit:
           if url in crawledPages or check_redirected_url(url) in crawledPages:
               toBeCrawledPages.remove(url)
               continue
           else:
               pg_no = inc()
               page = extract_html_page(url, pg_no)
               words = url.split("/", len(url))
               document_id = words[len(words)-1]
               print "document Id is " + document_id
               outlinks_of_page = extract_new_links(page)
               graph[document_id] = outlinks_of_page
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
        print len(toBeCrawledPages)
        temp = []
        for element in toBeCrawledPages:
            temp.append(element)
        crawled_limit = crawlPagesInToBeCrawled(temp)
        if crawled_limit == -1:
            return
    print "current level is greater than the level limit"
    return

def print_graph():
    print graph

def crawlSeed(seed):
    toBeCrawledPages.append(seed)
    startCrawling()
    listPagesCrawled(crawledPages)
    print_graph(graph)
def main():
    seed = input("enter seed url")
    crawlSeed(seed)
main()