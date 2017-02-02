import urllib2
from bs4 import BeautifulSoup as bs
import time
#variables and their initialization

pageCollectionLimit = 1000
sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
mainPage = "/wiki/Main_Page"
sustainableEnergyLinks = "D:/work/IR/assignment01/assignment_01_task2/sustainableEnergyLinks_Task2DFS.txt"
parent_node_stack = []
depthLimit = 1
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

def extract_new_links(page, keyword, head):
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
    print "new nodes in the extract function are" + str(child_node_count)
    parent_node_stack.append(head)
    for node in new_nodes:
        if node in crawledPages:
           print "already there"
           child_node_count -= 1
        if child_node_count == 0:
            return None
    else:
        push_into_stack(parent_node_stack,new_nodes, toBeCrawledPages)
    return child_node_count

def push_into_stack(parent_nodes, new_nodes, tbcl):
    while len(parent_nodes) > 0:
        tbcl.append(parent_nodes.pop())
    while len(new_nodes) > 0:
        node = new_nodes.pop()
        tbcl.append(node)
    return

def updateLevel():
    global currentLevel
    currentLevel += 1
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
    print "entered crawl head function"
    new_nodes_count = 0
    if len(crawledPages) < pageCollectionLimit:
        print "crawled pages is less than limit..."
        if head not in crawledPages or check_redirected_url(head) not in crawledPages:
            page = extract_html_page(head)
            new_nodes_count = extract_new_links(page, keyword, head)
            print "new nodes are " + str(new_nodes_count)
    else:
        return -1
    return new_nodes_count

def traverse_to_be_crawled_list_further(list, num_of_elements):
    print "entered the traversal of leaf elements"
    print "initial tobeCrawledList " + str(len(list))
    while num_of_elements > 0:
        print "depth count is "+ str(num_of_elements)
        if len(crawledPages) < pageCollectionLimit:
            head = list.pop()
            if head not in crawledPages or check_redirected_url(head) not in crawledPages:
                page = extract_html_page(head)
                crawledPages.append(head)
            num_of_elements -= 1
        else:
            print "crawling limit crossed"
            return -1
    print "now the TobeCrawledPages are" + str(len(toBeCrawledPages))
    print "now the crawledPages are " + str(len(crawledPages))
    return

def decrease_level():
    global currentLevel
    currentLevel -= 1
    return

def startCrawling(keyword):
    print "start crawling..."
    while currentLevel <= depthLimit :
        head = toBeCrawledPages.pop()
        crawl_limit = crawl_head(head, keyword)
        if crawl_limit == -1:
            print "1000 pages downloaded"
            return
        if crawl_limit == None:
            print "method returned none as answer"
            if len(toBeCrawledPages) > 0:
                print "to be crawled elements are not empty"
                continue
            else:
                traverse_to_be_crawled_list_further(parent_node_stack, len(parent_node_stack))
                "end of stack"
                return
        else:
            depth_count.append(crawl_limit)
            updateLevel()
    if currentLevel == depthLimit:
        if len(toBeCrawledPages) <= 0:
            "depth reached and no more pages to crawl so ended"
        return
    else:
        crawl_limit = traverse_to_be_crawled_list_further (toBeCrawledPages, depth_count.pop())
        if crawl_limit == -1:
            print "crawled 1000 pages and program ended"
            return
        decrease_level()
        startCrawling(keyword)
    return


def crawlSeed(seedUrl, keyword):
    toBeCrawledPages.append(seedUrl)
    startCrawling(keyword)
    listPagesCrawled(crawledPages)
def main():
    crawlSeed(seedUrl, keyword)

main()