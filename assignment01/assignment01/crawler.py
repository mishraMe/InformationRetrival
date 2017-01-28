import urllib
import HTMLParser

seedUrl = "https://en.wikipedia.org/wiki/Sustainable_energy"
handle = urllib.urlopen(seedUrl)
html_gunk = handle.read()

urlText = []
class parseText(HTMLParser.HTMLParser):

    def handle_data(self, data):
        if data != '\n':
            urlText.append(data)

lParser = parseText()
lParser.feed(html_gunk)
lParser.close();

for item in urlText:
    print item