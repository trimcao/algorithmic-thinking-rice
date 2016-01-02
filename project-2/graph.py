""" Project 1: Degree Distribution for Graph
Tri Minh Cao
trimcao@gmail.com
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])
             }
EX_GRAPH1 = {0: set([1,4,5]),
             1: set([6,2]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])
             }
EX_GRAPH2 = {0: set([1,4,5]),
             1: set([2,6]),
             2: set([7,3]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1,2]),
             9: set([0,3,4,5,6,7])
             }

def make_complete_graph(num_nodes):
    """ Make a complete directed graph with the input number of nodes."""
    graph = {}
    node_set = set([])
    for num in range (0, num_nodes):
        node_set.add(num)
    for index in range(0, num_nodes):
        temp_set = node_set.copy()
        temp_set.remove(index)
        graph[index] = temp_set
    return graph

def compute_in_degrees(digraph):
    """ Compute the in degree of each node in the digraph 
        and return as a dictionary """
    in_degrees = {}
    for each in digraph:
        degree = 0
        for each1 in digraph:
            if (each in digraph[each1]):
                degree += 1                
        in_degrees[each] = degree
    return in_degrees

def in_degree_distribution(digraph):
    """ Return the in degree distribution of the input directed graph."""
    in_degrees = compute_in_degrees(digraph)
    degree_dist = {}
    #for index in range(0, len(digraph) - 1):
    #    degree_dist[index] = 0
    for each in in_degrees: 
        if degree_dist.get(in_degrees[each]) is None:
            degree_dist[in_degrees[each]] = 1
        else:    
            degree_dist[in_degrees[each]] += 1
    return degree_dist


"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def normalized_in_degree(diagraph):
    normalized = in_degree_distribution(diagraph)
    length = 0
    for each in normalized:
        length += normalized[each]
    for each in normalized:
        normalized[each] /= float(length)
    return normalized

def out_degree_average(diagraph):
    total = 0
    for each in diagraph:
        total += len(diagraph[each])
    return total / len(diagraph)

def plot_normalized_log(digraph): 
    normalized = normalized_in_degree(citation_graph)
    #print normalized

    x = normalized.keys()
    y = normalized.values()
    fig, ax = plt.subplots()

    ax.loglog(x, y, basex = np.e, basey = np.e, linestyle='None', 
            marker='x', markeredgecolor='red')
    plt.xlabel("Log of in degrees, base e")
    plt.ylabel("Log of fraction of in degrees, base e")
    plt.title("Distribution of citations on a log scale")

    def ticks(y, pos):
        return r'$e^{:.0f}$'.format(np.log(y))

    ax.xaxis.set_major_formatter(mtick.FuncFormatter(ticks))
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(ticks))
    plt.show()

""" Question 1 for Application 1
"""
#citation_graph = load_graph(CITATION_URL)
#in_degree = compute_in_degrees(citation_graph)

#in_degree_test = compute_in_degrees(citation_graph)
#print in_degree_test    
#print out_degree_average(citation_graph)
"""
normalized = normalized_in_degree(citation_graph)
#print normalized

x = normalized.keys()
y = normalized.values()
fig, ax = plt.subplots()

ax.loglog(x, y, basex = np.e, basey = np.e, linestyle='None', 
           marker='x', markeredgecolor='red')
plt.xlabel("Log of in degrees, base e")
plt.ylabel("Log of fraction of in degrees, base e")
plt.title("Distribution of citations on a log scale")

def ticks(y, pos):
    return r'$e^{:.0f}$'.format(np.log(y))

ax.xaxis.set_major_formatter(mtick.FuncFormatter(ticks))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(ticks))
plt.show()

print "Finished!"
"""
