
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import random
#import graph 

def random_undirected_graph(num_nodes, p):
    """Generate a random undirected graph with probability p"""
    graph = {}
    for index in range(0, num_nodes):
        graph[index] = set([])
    for index in range(0, num_nodes):
        for number in range(0, num_nodes):
            if (index != number and (number not in graph[index])):
                a = random.random()
                if (a < p):
                    graph[index].add(number)
                    graph[number].add(index)
    return graph


def no_of_edges(ugraph):
    total = 0
    for node in ugraph:
        total += len(ugraph[node])
    return total/2

#test_graph = random_undirected_graph(1239, 0.002)
#print no_of_edges(test_graph)
#
#in_degree_test = compute_in_degrees(citation_graph)
#print in_degree_test    
#normalized = graph.normalized_in_degree(test_graph)
#print normalized
#
#x = normalized.keys()
#y = normalized.values()
#fig, ax = plt.subplots()
#
#ax.loglog(x, y, basex = np.e, basey = np.e, linestyle='None', 
#           marker='x', markeredgecolor='red')
#plt.xlabel("Log of in degrees, base e")
#plt.ylabel("Log of fraction of in degrees, base e")
#plt.title("Distribution of a random directed graph on log scale")
#
#def ticks(y, pos):
#    return r'$e^{:.0f}$'.format(np.log(y))
#
#ax.xaxis.set_major_formatter(mtick.FuncFormatter(ticks))
#ax.yaxis.set_major_formatter(mtick.FuncFormatter(ticks))
#plt.show()
#print "Finished!"
