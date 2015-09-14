# Constants
EX_GRAPH0 = {0: set([1, 2])}
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]),
             2: set([3]), 3: set([0]), 4: set([1]),
             5: set([2]), 6: set()}
EX_GRAPH2 = {0: set(1, 4, 5), 1: set([2, 6]),
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
                digragh.update({num: tem_set})
                            
    return digragh

def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph and computes the in degrees for
    the nodes in the graph
    """
    in_degree_dic = dict()
     
        
    return []

def in_degree_distribution(digragh):
    """
    Takes a directed graph digraph and computes the unnormalized
    distribution of the in-degrees of the graph
    """
    
    return []