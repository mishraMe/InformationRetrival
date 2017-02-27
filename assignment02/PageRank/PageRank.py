
#this program computes the page rank of a given page.

#populate pages in files if not done already
from collections import OrderedDict
all_pages = OrderedDict()
in_links = OrderedDict()
out_links = OrderedDict()
sinks = OrderedDict
graph2 = "graph2" #the existing file for Wt2g links
experiment = "experiment"
input_file = experiment
d = 0.85 #teleportation factor

#function to load data into the dictionaries
def load_data_in_dictionaries():
    file = open(input_file, 'r')
    lines = file.readlines()

    #populating in_links
    for line in lines:
        line = line.rstrip('\n')
        data = line.split(" ", len(line))
        key = data[0]
        data.remove(key)
        in_link_values = []
        for id in data:
            in_link_values.append(id)
        in_links[key] = in_link_values
    print " the inlinks are...."
    print in_links

    #populating outlinks
    for key in in_links.keys():
        for value in in_links.get(key):
            key2 = 0
            out_link_values = []
            if value in out_links.keys():
                print "entered the if on " + value
                out_links.get(value).append(key)
            else:
                key2 = value
                out_link_values.append(key)
                out_links[key2] = out_link_values
    print "outlinks are ..."
    print out_links

    #populate sinks
    sinks = []
    for key in in_links.keys():
        if (out_links.get(key) is None):
            sinks.append(key)
    print "sinks are ..."
    print sinks

    #populate all pages
    all_pages = []
    for key_in in in_links.keys():
        if(key_in not in all_pages):
            all_pages.append(key_in)
    for key_out in out_links.keys():
        if(key_out not in all_pages):
            all_pages.append(key_out)






















def main():
    load_data_in_dictionaries()

main()



# page rank