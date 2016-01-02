
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import random
import graph 

    
"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
   

def dpa_generator(n, m):
    """
    This method generates a random directed graph
    based on DPA algorithm
    Input: n nodes, m connections
    """
    new_graph = graph.make_complete_graph(m)
    dpa = DPATrial(m)
    for idx in range(m, n):
        neighbors = dpa.run_trial(m)
        new_graph[idx] = neighbors
    return new_graph
#First, test the DPA trial, sees what it does
"""
test_graph = graph.make_complete_graph(5)
dpa = DPATrial(5)
print dpa._num_nodes
print dpa._node_numbers
print dpa.run_trial(5)
print dpa._num_nodes
print dpa._node_numbers
print dpa.run_trial(5)
print dpa._num_nodes
print dpa._node_numbers
"""
    
pseudo_graph = dpa_generator(27770, 12)

normalized = graph.normalized_in_degree(pseudo_graph)
#print normalized

x = normalized.keys()
y = normalized.values()
fig, ax = plt.subplots()

ax.loglog(x, y, basex = np.e, basey = np.e, linestyle='None', 
           marker='x', markeredgecolor='red')
plt.xlabel("Log of in degrees, base e")
plt.ylabel("Log of fraction of in degrees, base e")
plt.title("Distribution of random-generated DPA graph on a log scale")

def ticks(y, pos):
    return r'$e^{:.0f}$'.format(np.log(y))

ax.xaxis.set_major_formatter(mtick.FuncFormatter(ticks))
ax.yaxis.set_major_formatter(mtick.FuncFormatter(ticks))
plt.show()

print "Finished!"

