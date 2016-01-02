
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import graph
"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

import random

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes) 
        #_num_nodes is the current node to add, note that a node is represented
        # only by a number
        for dummy_idx in range(len(new_node_neighbors)):
            # The below line differentiates UPA and DPA graph
            # In the UPA graph, the degree of an added node is not 0, but equal
            # to num_nodes
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def upa_generator(n, m):
    """
    This method generates a random directed graph
    based on UPA algorithm
    Input: n nodes, m connections
    """
    new_graph = graph.make_complete_graph(m)
    #print new_graph
    upa = UPATrial(m)
    for idx in range(m, n):
        neighbors = upa.run_trial(m)
        #print neighbors
        new_graph[idx] = neighbors
        for node in neighbors:
            new_graph[node].add(idx)
    return new_graph

#test_upa = upa_generator(7, 2)
#print test_upa

def no_of_edges(ugraph):
    total = 0
    for node in ugraph:
        total += len(ugraph[node])
    return total/2

#print test_upa
#print no_of_edges(test_upa)
#test_upa = upa_generator(1239, 3)
#print no_of_edges(test_upa)


