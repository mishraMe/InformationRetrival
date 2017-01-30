import urllib
import HTMLParser
import nltk
from bs4 import BeautifulSoup as bs
import time
#variables and their initialization
depthLimit = 1
currentLevel = 1
pageCollectionLimit = 1000
sleep_time = 1  # in seconds
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
prefix = "https://en.wikipedia.org"
crawledPages = []
toBeCrawledPages = [seedUrl]
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
            if not crawledPages.__contains__(final_url):
                toBeCrawledPages.append(final_url)
    return


def inc():
    global pg_no
    pg_no += 1
    return pg_no

def crawl():

    if crawledPages.__sizeof__() > pageCollectionLimit or currentLevel > depthLimit:
        return
    for url in toBeCrawledPages:
        if url not in crawledPages:
            pg_no = inc()
            page = extract_html_page(url, pg_no)
            extract_new_links(page)
            toBeCrawledPages.remove(url)
            crawledPages.append(url)
    return


def main():
    pg_no = 0
    crawl()
    return

main()