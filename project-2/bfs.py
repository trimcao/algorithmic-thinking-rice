"""
Project 2 
Algorithmic Thinking - Rice University @ Coursera
Tri Minh Cao
trimcao@gmail.com
September 2015
"""
from collections import deque

def bfs_visited(ugraph, start_node):
    """
    Using Breath-first search to find out connected set from a starting
    node
    """
    queue = deque()
    visited = set()
    visited.add(start_node)
    queue.append(start_node)
    while (len(queue) > 0):
       temp_node = queue.pop()
       for neighbor in ugraph[temp_node]:
           if neighbor not in visited:
               visited.add(neighbor)
               queue.append(neighbor)
    return visited

def cc_visited(ugraph):
    """
    Using BFS_visited method to find all the connected components of 
    an undirected graph
    """
    remain_nodes = ugraph.keys()
    connected_comps = [] # a list of sets
    while (len(remain_nodes) > 0):
        temp_node = remain_nodes[0] # choose an arbitrary node
        connected_set = bfs_visited(ugraph, temp_node)
        connected_comps.append(connected_set)
        for node in connected_set:
            remain_nodes.remove(node)
    return connected_comps

def largest_cc_size(ugraph):
    """
    Find the largest connected component size of an undirected graph
    """
    connected_comps = cc_visited(ugraph)
    largest = 0
    for each in connected_comps:
        if len(each) > largest:
            largest = len(each)
    return largest

def compute_resilience(ugraph, attack_order):
    """
    Compute the resilience of a network after an attack
    Find the largest connected component size through a list of attack 
    in order
    """
    #import ipdb
    #ipdb.set_trace()
    resilience = []
    resilience.append(largest_cc_size(ugraph))
    for each_node in attack_order:
        removed_edges = ugraph[each_node]
        remove_node(ugraph, each_node, removed_edges) 
        #print ugraph
        resilience.append(largest_cc_size(ugraph))
        #return_node(ugraph, each_node, removed_edges)
    return resilience

def remove_node(ugraph, node, edges):
    """
    Helper method to remove a node and its edges from an undirected graph
    """
    temp_ugraph = ugraph
    del temp_ugraph[node]
    #print temp_ugraph
    for each_key in edges:
        #print each_key
        #print temp_ugraph[each_key]
        temp_ugraph[each_key].remove(node) 

def return_node(ugraph, node, edges):
    """
    Helper method that return a node and its edges to re-construct 
    the original graph
    """
    temp_ugraph = ugraph
    temp_ugraph[node] = edges
    for each_key in edges:
        temp_ugraph[each_key].add(node)
    

EX_GRAPH1 = {0: set([1,4]),
             1: set([0,2]),
             2: set([1, 4]),
             3: set([5]),
             4: set([0, 2]),
             5: set([3]),
             6: set([])
             }

GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}
#visited = bfs_visited(EX_GRAPH1, 6)
#print visited
#connected_components = cc_visited(EX_GRAPH1)
#print connected_components
#print largest_cc_size(EX_GRAPH1)
#del EX_GRAPH1[1]
#print EX_GRAPH1
resi = compute_resilience(GRAPH0, set([1, 2]))
print resi

#test_set = set([2, 5])
#print test_set
#test_set.remove(2)
#print test_set

#test = deque()
#test.append(1)
#test.append(2)
#print test
#print test.pop()
#print test.pop()
#print len(test)
