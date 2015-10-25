"""
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
    index_range = range(len(cluster_list))
    idx1 = -1
    idx2 = -1
    dist = float("inf")
    for index1 in index_range:
        for index2 in index_range:
            if index2 == index1:
                continue
            else:
                tem_dist = pair_distance(cluster_list, idx1, idx2)[0]
                if tem_dist < dist:
                    dist = tem_dist
                    idx1 = index1
                    idx2 = index2
    return (dist, idx1, idx2)



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    length = len(cluster_list)
    if length <= 3:
        (dist, idx1, idx2) = slow_closest_pair(cluster_list)
    else:
        mid_index = length/2
        list_left = cluster_list[0:mid_index]
        list_right = cluster_list[mid_index:length]
        (distl, idx1l, idx2l) = fast_closest_pair(list_left)
        (distr, idx1r, idx2r) = fast_closest_pair(list_right)
        if distl < distr:
            (dist, idx1, idx2) = (distl, idx1l, idx2l)
        else:
            (dist, idx1, idx2) = (distr, idx1r, idx2r)
        center_line = (cluster_list[mid_index-1].horiz_center() + cluster_list[mid_index].horiz.center())/2
        (distc, idx1c, idx2c) = closest_pair_strip(cluster_list, center_line, dist)
        if distc < dist:
            (dist, idx1, idx2) = (distc, idx1c, idx2c) 
    return (dist, idx1, idx2)


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
    small_list = []
    for index in range(len(cluster_list)):
        if math.fabs(cluster_list[index].horiz_center() - horiz_center) < half_width:
            small_list += cluster_list[index]
    small_list.sort(key = lambda cluster: cluster.horiz_center())
    length = len(small_list)
    idx1 = -1
    idx2 = -1
    dist = float("inf")
    for index1 in range(length-1):
        upper = min([index1+3, length-1])
        for index2 in range(index1+1, upper+1):
            tem_dist = pair_distance(small_list, index1, index2)[0]
            if  tem_dist < dist:
                dist = tem_dist
                idx1 = index1
                idx2 = index2
    return (dist, idx1, idx2)
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        (dist, idx1, idx2) = fast_closest_pair(cluster_list)
        cluster_list[idx1].nerge_clusters(cluster_list[idx2])
        cluster_list.pop(idx2)
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
    length = len(cluster_list)
    # position initial clusters at the location of clusters with largest populations
    initial_list = []
    for index in range(length):
        if len(initial_list) < num_clusters:
            initial_list.append(cluster_list[index])
            initial_list.sort(key = lambda cluster: cluster.total_population())
        elif cluster_list[index].total_population() > initial_list[0].total_population():
            initial_list.pop(0)
            initial_list.append(cluster_list[index])
            initial_list.sort(key = lambda cluster: cluster.total_population())
    for dummy_num in range(num_iterations):
        re_cluster_list = []
        num = 0
        while num < num_clusters:
            re_cluster_list.append(alg_cluster.Cluster(set([]), 0, 0, 0, 0))
        for index1 in range(length):
            dist = float("inf")
            for index2 in range(num_clusters):
                if cluster_list[index1].distance(initial_list[index2]) < dist:
                    idx2 = index2
                else: continue
            re_cluster_list[idx2].merge_clusters(cluster_list[index1])
                
    return re_cluster_list

