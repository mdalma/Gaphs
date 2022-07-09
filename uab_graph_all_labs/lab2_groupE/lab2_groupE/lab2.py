#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:: Labs of Graphs, Topology, and Discrete Geometry - Data Engineering, UAB - 2019/2020 ::

Template for Lab2's tasks. See the assignment for details.

IMPORTANT: Don't change the provided function names, parameters or expected return.
"""

import itertools 
import networkx as nx
#import math
#import collections


def has_valid_frequencies(G):
    """If n is in G.nodes, you can access its frequency via:
        freq = G.nodes[n]["frequency"]

    This function should decide whether the frequency for each node is valid,
    as defined in the assignment.

    :param G: nx.Graph instance
    :return: True or False
    """    
    
    for node in G.nodes():        
        for neighbor in G.neighbors(node):
            #G.nodes[node]['count'] += 1           
            if G.nodes[node]['frequency'] == G.nodes[neighbor]["frequency"]:
                return False  
   

    return True
    #return G


#code to check how many times the node attribute is visited in the first two fors.
"""
oriol = nx.Graph()
[oriol.add_node(node, count = 0) for node in range(1, 1000)]

node2 = 1
for node1 in oriol.nodes():
    if node1 != node2:
        oriol.add_edge(node1, node2)
        node2 += 1
        
#Per a fer que alguns nodes tinguin més veins.       
oriol.add_edges_from([(3,5),(11,12),(11,15),(11,14)])           

G_sol = has_valid_frequencies(oriol)
for node in G_sol.nodes():
    print(f"Number of node: {node}")
    print(f"Node atribute times seen: {G_sol.nodes[node]['count']}")
    print(f"Neighbors: {list(G_sol.neighbors(node))}\n")
    
print(f"Total nodes of the graph: {len(oriol.nodes())}")
print(f"Total number of edges of the graph: {len(oriol.edges())}")  
""" 



def count_train_shelves(different_books, shelf_size):
    """Return the number of different shelves that can be created,
    as described in the assignment.

    :param different_books: the number of different books to be used
    :param shelf_size: total number of books in the self
    """
    return len([''.join(combinations) for combinations in itertools.combinations_with_replacement(different_books, shelf_size)])


    
def remove_subdivisions(G):
    """Return a version of G in which subdivisions are removed (undone),
    as described in the assignment.

    :param G: a nx.Graph instance
    """
    #We iterate over G_copy
    #We made changes over G
    #To avoid RuntimeError: dictionary changed size during iteration.
  
    G_copy = G.copy()
    for node in G_copy.nodes():
        #the node must have strictly two neighbors
        if G_copy.degree(node) == 2:
            #find out which are those two neighbors
            vei1, vei2 = G_copy.neighbors(node)
            #Remove that node (in the original graph)
            G.remove_node(node)
            #check if there is a connection between the neighbors of the deleted node
            if not G_copy.has_edge(vei1, vei2):
                #Connect the neighbors if they are not
                G.add_edge(vei1, vei2)
    
    #return the original graph (in which changes have been made) not the one we have used to iterate
    return G



def contains_K5_subgraph(G):
    """Return True if K5 is a subgraph of G (no need to remove edge subdivision)
    Otherwise, return False.
    """   
    #All posible combinatoris between the 5 nodes of the graph.
    for subnodes in itertools.combinations(G.nodes(), 5):
        #All posible subgraph for all possible combinatoris.
        subGraph = G.subgraph(subnodes)
        if len(subGraph.edges()) == 10:
            #Si algún subgraph de 5 nodes és complet (10 edges), serà K5.
            return True
        
    return False


def contains_K33_subgraph(G):
    """Return True if K3 is isomorphic to any subgraph of G
    (no need to remove edge subdivision)
    Otherwise, return False.
    """
    #El graph no és bipartite, no podrà ser K3
    if nx.algorithms.bipartite.is_bipartite(G) == False:
        return False
    
    #All posible combinatoris between the 6 nodes of the graph.
    for subnodes in itertools.combinations(G.nodes(), 6):
        #All posible subgraph for all possible combinatoris.
        subGraph = G.subgraph(subnodes)
        #Creation of bottom and top nodes of our bipartite subgraph.
        bottom_nodes, top_nodes = nx.algorithms.bipartite.sets(subGraph)
        
        #Assert there are 3 nodes in each set. (K_3,3)
        if (len(bottom_nodes) != 3 or len(top_nodes) != 3):
            return False
        
        compt_edges = 0 #Counter for total number of edges between both sets of nodes.
        #Assert all bottom_nodes are connected with all top_nodes.
        for bottom_node in bottom_nodes:
            for top_node in top_nodes:
                if subGraph.has_edge(bottom_node, top_node):
                    compt_edges += 1
        
        #k_3,3 must have 9 total esges between sets.
        return (compt_edges == 9)



