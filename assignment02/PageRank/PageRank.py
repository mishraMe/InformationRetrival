
#this program computes the page rank of a given page.

#populate pages in files if not done already
from collections import OrderedDict
import math
all_pages = []
in_links = OrderedDict()
out_links = OrderedDict()
sinks = []
graph2 = "graph2" #the existing file for Wt2g links
experiment = "experiment"
input_file = experiment
d = 0.85 #teleportation factor

#function to load data into the dictionaries
def load_data_in_dictionaries(graph):
    file = open(graph, 'r')
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
                out_links.get(value).append(key)
            else:
                key2 = value
                out_link_values.append(key)
                out_links[key2] = out_link_values
    print "outlinks are ..."
    print out_links

    #populate sinks
    for key in in_links.keys():
        if (out_links.get(key) is None):
            sinks.append(key)
    print "sinks are ..."
    print sinks

    #populate all pages
    for key_in in in_links.keys():
        if(key_in not in all_pages):
            all_pages.append(key_in)
    for key_out in out_links.keys():
        if(key_out not in all_pages):
            all_pages.append(key_out)
    print all_pages

# //	P	is	the	set	of	all	pages;	|P|	=	N
# //	S	is	the	set	of	sink	nodes,	i.e.,	pages	that	have	no	out	links
# //	M(p)	is the	set	(without	duplicates)	of	pages	that	link	to	page	p
# //	L(q)	is	the	number	of	out-links	(without	duplicates)	from	page	q
# //	d	is	the	PageRank	damping/teleportation	factor;	use	d	=	0.85	as	a	fairly	typical


def find_page_rank(graph):
    load_data_in_dictionaries(graph)
    page_rank = OrderedDict()
    new_page_rank = OrderedDict()
    P = all_pages
    N = len(all_pages)
    for page in P:
        page_rank[page] = 1/N
    pr_score = page_rank_converged(page_rank.values())
    while pr_score >= 1:
        sink_page_rank = 0
        for sink in sinks:
            sink_page_rank += page_rank.get(sink)
            #total sink page rank
        for page in all_pages:
            new_page_rank[page] = (1-d)/N
            new_page_rank[page] += d * sink_page_rank
            for in_link in in_links.get(page):
                new_page_rank[page] += d * page_rank.get(in_link)/out_links.get(in_link)
            for old_page in all_pages:
                page_rank[old_page] = new_page_rank[old_page]
        return pr_score

def page_rank_converged(page_ranks):
    entropy = calculate_entropy(page_ranks)
    print "entropy is... "
    print entropy
    perplexity = 2 ^ entropy
    return perplexity


def calculate_entropy(page_ranks):
    total = 0
    for rank in page_ranks:
        total += rank * 1
    entropy_value = 0 - total
    return entropy_value



def main():
    graph = input_file
    pr_score = find_page_rank(graph)
    print "page rank score is " + str(pr_score)
main()



# page rank