
"""
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: October 2015

Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    closest = (float("inf"), -1, -1)
    for idx1 in range(0, len(cluster_list)):
        for idx2 in range(0, len(cluster_list)):
            if (idx1 != idx2):
                distance = pair_distance(cluster_list, idx1, idx2)
                # distance is a tuple (distance, idx1, idx2)
                if (distance[0] < closest[0]):
                    closest = distance
    
    return closest



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    num_clusters = len(cluster_list)
    if (num_clusters <= 3):
        return slow_closest_pair(cluster_list)
    else:
        mid = num_clusters // 2
        left_list = cluster_list[:mid]
        right_list = cluster_list[mid:]
        left_closest = fast_closest_pair(left_list)
        right_closest = fast_closest_pair(right_list)
        # set the indices of the cluster in right_closest to the original
        # indices
        right_closest = (right_closest[0], right_closest[1] + mid, right_closest[2] + mid)
        # initiate closest = the closer between left_closest and right_closest
        closest = min(left_closest, right_closest, key = lambda x: x[0])
        # find the middle point for the middle strip
        mid_horiz = (cluster_list[mid - 1].horiz_center() + cluster_list[mid].horiz_center()) / 2
        # find the closest pair in the middle strip
        mid_closest = closest_pair_strip(cluster_list, mid_horiz, closest[0])
        # determinal the final closest pair
        closest = min(closest, mid_closest, key = lambda x: x[0])

    return closest


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    # get a list cluster_strip_y, all clusters in the middle strip
    # cluster_strip_y contains the index of the clusters in the original list
    # (not actual clusters)
    cluster_strip_y = [] # an empty list
    # find the clusters on the left of middle point
    for idx in range(0, len(cluster_list)):
        if (abs(cluster_list[idx].horiz_center() - horiz_center) < half_width):
            cluster_strip_y.append((cluster_list[idx], idx))
     
    # Sort cluster_strip_y based on vertical position
    cluster_strip_y.sort(key = lambda element: element[0].vert_center()) 
    #print cluster_strip_y
    num_clusters = len(cluster_strip_y)
    closest  = (float("inf"), -1, -1)
    # Scan to find the closest pair in the middle strip
    for idx1 in range(num_clusters - 1):
        # careful that the right_index for the range is the (last index + 1)
        right_index = min(idx1 + 8, num_clusters) 
        for idx2 in range(idx1 + 1, right_index):
            distance = pair_distance(cluster_list, cluster_strip_y[idx1][1], cluster_strip_y[idx2][1])
            #print distance
            # distance is a tuple (distance, idx1, idx2)
            if (distance[0] < closest[0]):
                closest = distance

    return closest
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    # we need to sort the clusters based on horizontal center 
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    current_num_cluster = len(cluster_list)
    # start the loop to reduce the number of clusters
    while (current_num_cluster > num_clusters):
       closest_pair = fast_closest_pair(cluster_list)
       cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])
       # remove old clusters
       cluster_list.pop(closest_pair[2])
       # re-sort the cluster list
       cluster_list.sort(key = lambda cluster: cluster.horiz_center())
       # update current_num_cluster
       current_num_cluster = len(cluster_list)
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    length_cluster_list = len(cluster_list)
    # position initial clusters at the location of clusters with largest populations
    # initialize each center to (0, 0)
    centers = [(0, 0) for idx in range(num_clusters)]
    # find the clusters with the largest populations
    max_index = []
    current_max = -1
    index = -1
    # set the centers as the locations with largest populations
    for idx in range(num_clusters):
       current_max = -1
       index = -1
       for idx2 in range(length_cluster_list):
           population = cluster_list[idx2].total_population()
           if ((population > current_max) and (idx2 not in max_index)):
               index = idx2
               current_max = cluster_list[idx2].total_population()
       centers[idx] = (cluster_list[index].horiz_center(), cluster_list[index].vert_center())
       max_index.append(index)

    # initialize the final cluster list
    final_list = []
    # iterate to find the clustes and update the centers
    for dummy_idx in range(num_iterations):
        final_list = []
        # create a number of empty cluster
        for dummy_idx2 in range(num_clusters):
            final_list.append(alg_cluster.Cluster(set([]), centers[idx][0], centers[idx][1], 0, 0))
        # process each point 
        for idx in range(length_cluster_list):
            closest_center = min_dist_center(cluster_list[idx], centers)
            # merge the current point to the cluster
            final_list[closest_center].merge_clusters(cluster_list[idx])
        # update the centers
        for idx in range(num_clusters):
            centers[idx] = (final_list[idx].horiz_center(), final_list[idx].vert_center())
    return final_list

def min_dist_center(cluster, center_list):
    """
    Method to find the index of the center in a center list that has the minimal
    distance to the cluster
    """
    min_distance = float("inf")
    index = -1
    for idx in range(len(center_list)):
        center = center_list[idx]
        distance_squared = (center[0] - cluster.horiz_center())**2 + (center[1] - cluster.vert_center())**2 
        if (distance_squared < min_distance):
            min_distance = distance_squared
            index = idx
    return index
######################################################################
# Test
#print slow_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0)])
#print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)], 1.5, 1.0)
#print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 0, 1, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 1, 1, 0)], 0.5, 1.0)
#print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)]) 
#print fast_closest_pair([alg_cluster.Cluster(set([]), 0.23, 0.94, 1, 0), alg_cluster.Cluster(set([]), 0.65, 0.08, 1, 0), alg_cluster.Cluster(set([]), 0.66, 0.43, 1, 0), alg_cluster.Cluster(set([]), 0.91, 0.6, 1, 0), alg_cluster.Cluster(set([]), 0.94, 0.9, 1, 0)])
