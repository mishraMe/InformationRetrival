
# corpus generator generates a cleaned corpus, free of any HTML tags,
# URLs, or pictures, references to images, etc

from bs4 import BeautifulSoup as bs, NavigableString
import os
import re
from unidecode import unidecode
content = "content_dir/"
cleaned_content = "cleaned_content_dir/"
new_page = ""


def generate_corpus():
    files = os.listdir(content)
    title = ""
    cleaned_page = ""
    for filename in files:
        page = open(content + filename, "r+")
        cleaned_page, title = clean_page(page)
        store_page(cleaned_page, title)
    return cleaned_page, title

head = "url : https://en.wikipedia.org/wiki/"


def clean_page(unclean_page):
    global new_page
    title_text = unclean_page.readline()
    title = title_text.strip(head).strip('\n')
    special_characters = ["_", "-", ":", "/", "//", "!",
                          "?", "#", "^", "*", "~", "&",
                          "(", ")", "[", "]", "{", "}",
                          "'", ";", '"', "$", "%" "|"]
    for each in special_characters:
        title = title.replace(each, "")
    soup = bs(unclean_page.read(), 'html.parser')
    for val in soup.find_all(['head', 'script', 'style', 'table']):
        val.extract()
    for link in soup.find_all("a"):
        href_val = link.get("href")
        if href_val is not None:
            if ".jpg" in href_val or ".jpeg" in href_val or ".asp" in href_val\
                    or ".gif" in href_val or ".png" in href_val\
                    or "?" in href_val:
                link.extract()
    for link in soup.find_all(attrs={"role": "navigation"}):
        link.extract()
    for each in soup.find_all(attrs={"id": "jump-to-nav"}):
        each.extract()
    for each in soup.find_all(attrs={"id": "siteSub"}):
        each.extract()
    for each in soup.find_all(attrs={"id": "References"}):
        each.extract()
    for each in soup.find_all(attrs={"class": "references"}):
        each.extract()
    for each in soup.find_all(attrs={"class": "mw-head"}):
        each.extract()
    for each in soup.find_all(attrs={"id": "footer"}):
        each.extract()
# or everything else but paragraphs and titles
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    text = '\n'.join(line for line in lines if line)
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.encode('utf-8')
    text = text.lower()
    for each in special_characters:
        text = text.replace(each, '')
    text = re.sub('(?<=\D)[.,]|[.,](?=\D)', '', text)
    text = re.sub('(?<![A-Za-z])[-]|[-](?![A-Za-z])', '', text)
    cleaned_page = text
    return cleaned_page, title


def store_page(page, title):
    print title
    if title is "":
        return
    cleaned_page_file = open(cleaned_content + "/" + title, 'w+')
    cleaned_page_file.writelines(page)
    cleaned_page_file.close()

    return


def main():
    page, title = generate_corpus()

main()



