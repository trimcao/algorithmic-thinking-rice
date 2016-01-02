"""
Algorithmic Thinking - Application 3
Closest Pairs and Clustering Algorithms
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: October 2015
"""

import random
import math
import project3
import alg_cluster
import time
import cluster_visual
# Desktop imports
import matplotlib.pyplot as plt

def gen_random_clusters(num_clusters):
    """
    Generate random clusters, each corresponds to a point in a square
    with corners (+-1, +-1)
    """
    cluster_list = []
    for dummy_idx in range(num_clusters):
        # generate a random point on x-axis in range[-1, 1) 
        horiz = random.random() * (1.0 - (-1.0)) + (-1.0)
        vert = random.random() * (1.0 - (-1.0)) + (-1.0)
        cluster_list.append(alg_cluster.Cluster(set([]), horiz, vert, 1, 0))
    return cluster_list

def question_1():
    """
    Compare the running times of slow_closest_pair and fast_closest_pair
    methods using gen_random_clsuters function
    """
    # generate a list of lists of clusters with size 2 to 200
    cluster_compare = []
    for size in range(2, 200 + 1):
        cluster_compare.append(gen_random_clusters(size))
        
    # get the running time of both methods
    time_fast_method = []
    time_slow_method = []
    for each_list in cluster_compare:
        start_time = time.time()
        project3.fast_closest_pair(each_list)
        elapsed_time = time.time() - start_time
        time_fast_method.append(elapsed_time)
        # add running time for slow_closest_pair
        start_time = time.time()
        project3.slow_closest_pair(each_list)
        elapsed_time = time.time() - start_time
        time_slow_method.append(elapsed_time)
    
    # values for the x-axis
    num_lists = range(2, 200 + 1)
    # Plot data

    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(8,8), dpi=80)

    # Create a new subplot from a grid of 1x1
    plt.subplot(1,1,1) #parameters: row, column, location index

    plt.xlabel("Size of the Cluster List")
    plt.ylabel("Time Elapsed")
    plt.title("Comparasion of Two Closest-pair-finding Methods (on Desktop)")
    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(num_lists, time_fast_method, color="blue", linewidth=2.0, linestyle="-", label="Fast Closest Pair")

    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(num_lists, time_slow_method, color="green", linewidth=2.0, linestyle="-", label="Slow Closest Pair")

    # Add Legends
    plt.legend(loc='upper left', frameon=False)
    # Show result on screen
    plt.show()

########################################
# Compute Distortion 
def compute_distortion(cluster_list, data_table):
    distortion = 0
    for each in cluster_list:
        distortion += each.cluster_error(data_table)
    return distortion

def question_10():
    """
    Compare the quality of two clustering methods by comparing distortion
    produced by the two.
    """
    
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
    # choose the data file
    data_table = cluster_visual.load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    num_clusters = range(6, 20 + 1)
    distortion_k_means = []
    distortion_hier = []

    # compute distortion values for k-means clustering
    for each_num in num_clusters:
        cluster_list = project3.kmeans_clustering(singleton_list, each_num, 5)
        distortion_k_means.append(compute_distortion(cluster_list, data_table))

    # compute distortion values for hierarchical clustering
    hier_clusters = singleton_list
    for num_clus in range(20, 5, -1):
        hier_clusters = project3.hierarchical_clustering(hier_clusters, num_clus)
        distortion_hier.append(compute_distortion(hier_clusters, data_table))
    # reverse the distortion_hier list
    distortion_hier.reverse()
    
    # plot the results
    
    # Create a new figure of size 8x6 points, using 100 dots per inch
    plt.figure(figsize=(8,8), dpi=80)

    # Create a new subplot from a grid of 1x1
    plt.subplot(1,1,1) #parameters: row, column, location index

    plt.xlabel("Number of Clusters")
    plt.ylabel("Distortion")
    plt.title("Quality comparison - Two Clustering Methods - 111 Data")
    # Plot cosine using blue color with a continuous line of width 1 (pixels)
    plt.plot(num_clusters, distortion_k_means, color="blue", linewidth=2.0, linestyle="-", label="k-means")

    # Plot sine using green color with a continuous line of width 1 (pixels)
    plt.plot(num_clusters, distortion_hier, color="green", linewidth=2.0, linestyle="-", label="hierarchical")

    # Add Legends
    plt.legend(loc='upper right', frameon=False)
    # Show result on screen
    plt.show()

#question_1()
question_10()
# test gen_random_clusters
#test = gen_random_clusters(4)
#print len(test)
