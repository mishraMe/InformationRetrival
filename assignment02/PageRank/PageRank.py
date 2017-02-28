
#this program computes the page rank of a given page.

#populate pages in files if not done already
from collections import OrderedDict
import math
#global variables
all_pages = []
in_links = OrderedDict()
out_links = OrderedDict()
sinks = []
old_perplexity = 0.0
new_perplexity = 0.0
convergence = 0.0
graph2 = "graph2" #the existing file for Wt2g links
experiment = "experiment"
input_file = experiment
d = 0.85 #teleportation factor

#function to load data into the dictionaries
def load_data_in_dictionaries(graph):
    print "entered the load function"
    global all_pages
    file = open(graph, 'r')
    lines = file.readlines()

    #populating in_links
    for line in lines:
        line = line.rstrip('\n')
        data = line.split(" ", len(line))
        key = data[0]
        data.remove(key)
        in_link_values = []
        for i in data:
            in_link_values.append(i)
        in_links[key] = in_link_values
    print " the inlinks are...."
    # print in_links

    #populating outlinks
    print "calculating the outlinks"
    for key in in_links:
        for value in in_links[key]:
            out_link_values = []
            if value in out_links:
                out_links[value].append(key)
            else:
                key2 = value
                out_link_values.append(key)
                out_links[key2] = out_link_values
    print "outlinks are ..."
    # print out_links

    #populate sinks
    print "calculating the sinks"
    for key in in_links:
        if (out_links.get(key) is None):
            sinks.append(key)
    print "sinks are ..."
    # print sinks

    #populate all pages
    print "calculating the all pages"
    for key_in in in_links:
            all_pages.append(key_in)
    for key_out in out_links:
            all_pages.append(key_out)

    all_pages = set(all_pages)
    # print all_pages
    return 0

# //	P	is	the	set	of	all	pages;	|P|	=	N
# //	S	is	the	set	of	sink	nodes,	i.e.,	pages	that	have	no	out	links
# //	M(p)	is the	set	(without	duplicates)	of	pages	that	link	to	page	p
# //	L(q)	is	the	number	of	out-links	(without	duplicates)	from	page	q
# //	d	is	the	PageRank	damping/teleportation	factor;	use	d	=	0.85	as	a	fairly	typical


def find_page_rank(graph):
    global old_perplexity
    global new_perplexity
    page_rank = OrderedDict()
    new_page_rank = OrderedDict()
    P = all_pages
    N = len(all_pages)
    change = 0.0
    count = 0

    for page in P:
        page_rank[page] = 1.0/N

    while(change >= 1.0 and change is not 0.0) or count < 4:
        sink_page_rank = 0.0
        for sink in sinks:
            sink_page_rank += page_rank[sink]
            #total sink page rank
        for page in all_pages:
            new_page_rank[page] = (1.0-d)/N
            new_page_rank[page] += d * sink_page_rank/N
            if page not in in_links:
                continue
            for in_link in in_links[page]:
                length_out_links = len(out_links[in_link])
                new_page_rank[page] += d * (page_rank[in_link]/length_out_links)
        for old_page in all_pages:
            page_rank[old_page] = new_page_rank.get(old_page)
        # page ranks are changed
        new_perplexity = calculate_perplexity(page_rank.values())
        change = page_rank_converged(old_perplexity, new_perplexity)
        if change < 1.0:
            count += 1
        else:
            count = 0
        old_perplexity = new_perplexity
    return page_rank

def page_rank_converged(old_perplexity, new_perplexity):
    change = new_perplexity - old_perplexity
    print "perplexity change is " + str(change)
    return change

def calculate_perplexity(page_ranks):
    entropy = calculate_entropy(page_ranks)
    perplexity = 2.0**entropy
    return perplexity


def calculate_entropy(page_ranks):
    entropy_value = 0
    for rank in page_ranks:
        if rank is not 0:
            entropy_value += rank * math.log(1/rank, 2)
    return entropy_value



def main():
    graph = input_file
    load_data_in_dictionaries(graph)
    pr_score = find_page_rank(graph)
    print "page rank score is " + str(pr_score)
main()
# page rank