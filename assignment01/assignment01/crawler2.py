import urllib
import HTMLParser
import nltk
from bs4 import BeautifulSoup as bs

#save the seed page content in a variable

depthLimit = 5
currentLevel = 1
pageCollectionLimit = 1000
politenessFactor = 1  # in seconds
crawled = []
toBeCrawled = []
seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
seedPage = urllib.urlopen(seedUrl).read()
file = open("D:/work/IR/assignment01/seedPage.txt", "w+")
file.writelines("url :" + seedUrl + '\n' + seedPage)
file.close()

# we saved the crawled page in the above lines and saved the raw html with its URL in a file.
# next we create a soup of the same and try to extract valuable inforamtion like new links to crawl
soup = bs(seedPage, 'html.parser')
content = str(soup)

def find_links():
    child_links = []
    for tag in soup.find_all('a'):
        href = tag.get("href")
        if href is not None and ":" not in href and "#" not in href:
            child_links.append(tag.get("href"))

    for a_link in child_links:
        print a_link

    return

def main():
    find_links()

main()
