
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import random
import graph 

def random_directed_graph(num_nodes, p):
    """Generate a random directed graph with probability p"""
    graph = {}
    for index in range(0, num_nodes):
        graph[index] = set([])
        for number in range(0, num_nodes):
            if (index != number):
                a = random.random()
                if (a < p):
                    graph[index].add(number)
    return graph

test_graph = random_directed_graph(10000, 0.5)
#print test_graph

#in_degree_test = compute_in_degrees(citation_graph)
#print in_degree_test    
normalized = graph.normalized_in_degree(test_graph)
#print normalized

x = normalized.keys()
y = normalized.values()
fig, ax = plt.subplots()

ax.loglog(x, y, basex = np.e, basey = np.e, linestyle='None', 
           marker='x', markeredgecolor='red')
plt.xlabel("Log of in degrees, base e")
plt.ylabel("Log of fraction of in degrees, base e")
plt.title("Distribution of a random directed graph on log scale")

def ticks(y, pos):
    return r'$e^{:.0f}$'.format(np.log(y))

ax.xaxis.set_major_formatter(mtick.FuncFormatter(ticks))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(ticks))
plt.show()
print "Finished!"
