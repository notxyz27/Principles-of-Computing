"""
Algorithmic Thinking Project 1
"""
# Constants
EX_GRAPH0 = {0: set([1, 2]), 1: set(), 2: set()}
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]),
             2: set([3]), 3: set([0]), 4: set([1]),
             5: set([2]), 6: set()}
EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]),
             2: set([3, 7]), 3: set([7]), 4: set([1]),
             5: set([2]), 6: set(), 7: set([3]),
             8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary
    corresponding to a complete directed gragh
    """
    digragh = dict()
    
    if num_nodes > 0:
            for num in range(num_nodes):
                tem_list = range(num_nodes)
                tem_list.remove(num)
                tem_set = set(tem_list)
                digragh[num] = tem_set
                            
    return digragh

def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph and computes the in degrees for
    the nodes in the graph
    """
    in_degree_dic = dict()
    
    keys = digraph.keys()
    for key in keys:
        in_degree_dic[key] = 0
    for edge_set in  digraph.values():
        for tail in edge_set:
            in_degree_dic[tail] += 1
    """
    for key in digraph.keys():
        degree = 0
        for node, edges in digraph.items():
            if node == key:
                continue
            elif key in edges:
                degree += 1
        in_degree_dic[key] = degree
    """
    return in_degree_dic

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph and computes the unnormalized
    distribution of the in-degrees of the graph
    """
    digraph_degree = compute_in_degrees(digraph)
    in_degree_dist = dict()
    num_node = float(len(digraph))
    
    for value in digraph_degree.values():
        if value not in in_degree_dist.keys():
            in_degree_dist[value] = 1
        else:
            in_degree_dist[value] += 1
    
    for node, degree in in_degree_dist.items():
        in_degree_dist[node] = degree/num_node
    """
    for key in range(0, len(digraph_degree)):
        count = 0
        for degree in digraph_degree.values():
            if degree == key:
                count += 1
                
        if count > 0:
            in_degree_dist[key] = count/num_node
    """               
    return in_degree_dist

