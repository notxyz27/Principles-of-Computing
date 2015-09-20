"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
from user40_VFBeihtqqa_45 import *
import simpleplot
import math

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(45)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

def build_plot(digraph):
    plot = []
    for key, value in digraph.items():
        if key != 0:
            plot.append([math.log(key, 2), math.log(value, 2)])
    return plot

citation_graph = load_graph(CITATION_URL)
distribution = in_degree_distribution(citation_graph)

distribution_plot = build_plot(distribution)
simpleplot.plot_lines("Citation in-degree distribution", 
                      600, 600, "Logarithm of in-degree",
                      "Logarithm of counts", [distribution_plot], 
                      True, ["Citation in-degree distribution"])

