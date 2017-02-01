import urllib2
from bs4 import BeautifulSoup as bs
import time
#variables and their initialization

pageCollectionLimit = 1000
sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
mainPage = "/wiki/Main_Page"
sustainableEnergyLinks = "D:/work/IR/assignment_01_task2/sustainableEnergyLinks_Task2.txt"
depthLimit = 5
currentLevel = 1
depth_count = [1]
crawledPages = []
toBeCrawledPages = []
keyword = "solar"
pg_no = 0
#the below function is used to extract raw html of the page to be saved

def extract_html_page(full_url):
    time.sleep(sleep_time)
    page = urllib2.urlopen(full_url).read()
    return page

def extract_new_links(page, keyword):
    child_node_count = 0
    new_nodes = []
    soup = bs(page, 'html.parser')
    for tag in soup.find_all('a'):
        href = tag.get("href")
        content = tag.text
        if href is not None and "/wiki/" in href:
            if ":" in href or "#" in href or "." in href or "?" in href or href == mainPage:
                continue
            else:
                if keyword.lower() in content.lower() or keyword.lower() in href.lower():
                    child_node_count += 1
                    final_url = prefix + href
                    new_nodes.append(final_url)
    toBeCrawledPages.extend(new_nodes)
    return child_node_count

def updateLevel():
    global currentLevel
    currentLevel += 1
    print currentLevel
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

def crawl_head(head, keyword):
    new_nodes_count = 0
    if len(crawledPages) < pageCollectionLimit:
        if head not in crawledPages or check_redirected_url(head) not in crawledPages:
            page = extract_html_page(head)
            new_nodes_count = extract_new_links(page, keyword)
            crawledPages.append(head)
    else:
        return -1
    return new_nodes_count

def traverse_to_be_crawled_list_further(list, depth_count):
    while depth_count > 0:
        if len(crawledPages) < pageCollectionLimit:
            head = list.pop()
            if head not in crawledPages or check_redirected_url(head) not in crawledPages:
                page = extract_html_page(head)
                crawledPages.append(head)
            depth_count -= 1
        else: return -1
    return

def decrease_level():
    global currentLevel
    currentLevel -= 1
    return

def startCrawling(keyword):
    while currentLevel <= depthLimit:
        head = toBeCrawledPages.pop()
        crawl_limit = crawl_head(head, keyword)
        if crawl_limit == -1:
            print "1000 pages downloaded"
            return
        if crawl_limit == 0:
            depth_count.extend(crawl_limit)
            continue
        else:
            depth_count.extend(crawl_limit)
            updateLevel()
    if len(toBeCrawledPages)<=0:
        "depth rached and no more pages to crawl so ended"
        return
    else:
        crawl_limit = traverse_to_be_crawled_list_further (toBeCrawledPages, depth_count.pop())
        if crawl_limit == -1:
            print "crawled 1000 pages and program ended"
            return
        decrease_level()
        startCrawling(keyword)


def crawlSeed(seedUrl, keyword):
    toBeCrawledPages.append(seedUrl)
    startCrawling(keyword)
    listPagesCrawled(crawledPages)
def main():
    crawlSeed(seedUrl, keyword)

main()