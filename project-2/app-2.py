
"""
Application portion of Module 2
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: September 2015
"""

# general imports
import urllib2
import random
import time
import math
import upa
import er_und
import bfs
# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
def random_order(ugraph):
    nodes = ugraph.keys()
    random.shuffle(nodes)
    return nodes

def fast_targeted_order(ugraph):
    # create a new graph by copying
    new_graph = copy_graph(ugraph)
    degree_sets = {}
    for idx in range(len(new_graph)):
        degree_sets[idx] = set()
    for node in new_graph: 
        degree_sets[len(new_graph[node])].add(node)
    
    #degree_132 = len(new_graph[132])
    #print len(new_graph[132])
    ##print degree_132
    #print degree_sets[degree_132]
    target_list = []
    index = 0

    for degree in range(len(degree_sets) - 1, -1, -1):
        while (len(degree_sets[degree]) > 0):
            current_node = degree_sets[degree].pop()
            #degree_sets[degree].remove(current_node)
            for neighbor in new_graph[current_node]:
                neighbor_degree = len(new_graph[neighbor])
                degree_sets[neighbor_degree].remove(neighbor)
                degree_sets[neighbor_degree - 1].add(neighbor)
            # add the current node to target list
            target_list.append(current_node)
            # remove current node from ugraph
            delete_node(new_graph, current_node)
    return target_list
        
##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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

#example_network = load_graph(NETWORK_URL)
#print len(example_network)
#network_attack = fast_targeted_order(example_network)
##########################################
# PLOT THE DATA#
def question_1():
    # THE CORRECT probability factor p for er_undirected should be 0.002
    # also, I SHOULD HAVE LISTED the values of p and m
    example_network = load_graph(NETWORK_URL)
    er_undirected = er_und.random_undirected_graph(1239, 0.002)
    upa = upa.upa_generator(1239, 3)
    
    er_attack = random_order(er_undirected)
    upa_attack = random_order(upa)
    network_attack = random_order(example_network)
    
    er_resilience = bfs.compute_resilience(er_undirected, er_attack)
    upa_resilience = bfs.compute_resilience(upa, upa_attack)
    network_resilience = bfs.compute_resilience(example_network, network_attack)
    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(10,6), dpi=80)

    # Create a new subplot from a grid of 1x1
    plt.subplot(1,1,1) #parameters: row, column, location index

    plt.xlabel("Number of removed nodes")
    plt.ylabel("Size of the Largest Component")
    plt.title("The Resilience of Different Types of Networks")
    # Generate points
    X = [n for n in range(len(er_resilience))]
    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(X, er_resilience, color="blue", linewidth=2.0, linestyle="-", label="ER Graph")

    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(X, upa_resilience, color="green", linewidth=2.0, linestyle="-", label="UPA Graph")

    plt.plot(X, network_resilience, color="red", linewidth=2.0, linestyle="-", label="Example Network")
    # Add Legends
    plt.legend(loc='upper right', frameon=False)
    # Show result on screen
    plt.show()

######################################
# QUESTION 2
def question_2():
    graph_list = []
    # generate UPA graphs with n in range(10, 1000) and m = 5
    for num_nodes in range(10, 1000, 10):
        graph_list.append(upa.upa_generator(num_nodes, 5))
    
    num_nodes = [idx for idx in range(10, 1000, 10)]
    time_fast_target = []
    time_normal_target = []
    for each_graph in graph_list:
        start_time = time.time()
        fast_targeted_order(each_graph)
        elapsed_time = time.time() - start_time
        time_fast_target.append(elapsed_time)
        start_time = time.time()
        targeted_order(each_graph)
        elapsed_time = time.time() - start_time
        time_normal_target.append(elapsed_time)

    # Plot data

    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(8,8), dpi=80)

    # Create a new subplot from a grid of 1x1
    plt.subplot(1,1,1) #parameters: row, column, location index

    plt.xlabel("Number of Nodes")
    plt.ylabel("Time Elapsed")
    plt.title("Comparasion of Two Target-finder Methods (on Desktop)")
    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(num_nodes, time_fast_target, color="blue", linewidth=2.0, linestyle="-", label="Fast Targeted Order")

    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(num_nodes, time_normal_target, color="green", linewidth=2.0, linestyle="-", label="(Normal) Targeted Order")

    # Add Legends
    plt.legend(loc='upper left', frameon=False)
    # Show result on screen
    plt.show()

def question_4():
    example_network = load_graph(NETWORK_URL)
    er_undirected = er_und.random_undirected_graph(1239, 0.002)
    upa_graph = upa.upa_generator(1239, 3)
    
    er_attack = fast_targeted_order(er_undirected)
    upa_attack = fast_targeted_order(upa_graph)
    network_attack = fast_targeted_order(example_network)
    
    er_resilience = bfs.compute_resilience(er_undirected, er_attack)
    upa_resilience = bfs.compute_resilience(upa_graph, upa_attack)
    network_resilience = bfs.compute_resilience(example_network, network_attack)
    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(8,6), dpi=80)

    # Create a new subplot from a grid of 1x1
    plt.subplot(1,1,1) #parameters: row, column, location index

    plt.xlabel("Number of removed nodes")
    plt.ylabel("Size of the Largest Component")
    plt.title("The Resilience of Different Types of Networks - using Targeted Order")
    # Generate points
    X = [n for n in range(len(er_resilience))]
    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(X, er_resilience, color="blue", linewidth=2.0, linestyle="-", label="ER Graph")

    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(X, upa_resilience, color="green", linewidth=2.0, linestyle="-", label="UPA Graph")

    plt.plot(X, network_resilience, color="red", linewidth=2.0, linestyle="-", label="Example Network")
    # Add Legends
    plt.legend(loc='upper right', frameon=False)
    # Show result on screen
    plt.show()

# ANSWER THE QUESTIONS
# time.time() returns the time as seconds
#question_2()
question_4()
