#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:: Labs of Graphs, Topology, and Discrete Geometry - Data Engineering, UAB - 2019/2020 ::

Example (incomplete) unit tests for Lab2. Students are expected to add and submit their own test implementations. 

NOTE: new tests can be added to the TestLab subclass defined here, starting with def test_, accepting one parameter (self), and with the right indentation, e.g.,
   def test_new_test1(self):
        assert False
"""

import sys
import os
import unittest
import networkx as nx
import random
import numpy as np
import itertools
from time import time
from test_lab import TestLab
#import matplotlib.pyplot as plt


class TestLab2(TestLab, unittest.TestCase):
    name = "lab2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_frequencies(self):
        """Verify that adjacent nodes have different frequencies, for graphs that
        meet the condition (neighbors: different "frequency" attribute)
        """
        
        print("TEST VALID FREQUENCIES...\n") 
        valid_frequencies_func = self.released_module.lab2.has_valid_frequencies
        
        #Graph in which every adjacent node have a diferent frequency atribute.
        miquel = nx.Graph()
        [miquel.add_node(node, frequency = 0) for node in range(1, 1000)]
        
        used_frequencies = []
        node2 = 1
        
        for node1 in miquel.nodes():
            if node1 != node2:
                miquel.add_edge(node1, node2)
                node2 += 1
              
            current_frequency = random.randint(1, 100000000)
            while current_frequency in used_frequencies:
                current_frequency = random.randint(1, 100000000)
              
            used_frequencies.append(current_frequency)
            miquel.nodes[node1]['frequency'] = current_frequency
        
        #print(len(miquel.edges()))
        #print(len(miquel.nodes()))
            
        expected_result = True         
        print(f"Test for valid frequencies is (True == passed): {valid_frequencies_func(miquel) == expected_result}")
          
        #Expected result = False
        #Graph which adjacent nodes have the same frequency atribute.
        oriol = nx.Graph()
        [oriol.add_node(node, frequency = 0) for node in range(1, 1000)]
        
        node2 = 1
        for node1 in oriol.nodes():
            if node1 != node2:
                oriol.add_edge(node1, node2)
                node2 += 1
                           
            oriol.nodes[node1]['frequency'] = random.randint(1, 20)
        
        #print(len(oriol.edges()))
        #print(len(oriol.nodes()))
        
        expected_result = False        
        print(f"Test for valid frequencies is (True == passed): {valid_frequencies_func(oriol) == expected_result}\n\n")
      


    def test_unique_shelves(self):
        possible_shelves_func = self.released_module.lab2.count_train_shelves
        print("TEST UNIQUE SHLEVES...\n")             
        #TEST FOR SMALL SIZES
        print("1. Starting test for small sizes...")
        excpected_output_small_sizes = 10 #Calculated with the formula.
        function_output_small_sizes = possible_shelves_func('ABCD', 2)
        
        print(f"For small sizes, the function output is --> {function_output_small_sizes == excpected_output_small_sizes}\n")
        
        #TEST FOR BIG SIZES
        print("1.1. Starting test for big sizes...")
        excpected_output_big_sizes = 906192 #Calculated with the formula.
        function_output_big_sizes = possible_shelves_func('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ', 6)
        
        print(f"For big sizes, the function output is --> {function_output_big_sizes == excpected_output_big_sizes}\n")
        
        
        #Test time change with different_books or shelf_sizes.
        print("2. Test time change with different_books or shelf_sizes...\n\n2.1. With big 'B' (B=27, S=6):")
        start_time1 = time()
        possible_shelves_func('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ', 6)
        final_time1 = time()
        total_time1 = final_time1 - start_time1 
        print(f"The total time of the execution was of --> {total_time1}\n")
        
        print("2.2. With big 'S' (B=6, S=27):")
        start_time2 = time()
        possible_shelves_func('ABCDEF', 27)
        final_time2 = time()
        total_time2 = final_time2 - start_time2
        print(f"The total time of the execution was of --> {total_time2}\n")
        
        if total_time1 > total_time2:
            print("The execution time is higher for huge B.\n\n")
        else:
            print("The execution time is higher for huge S.\n\n")
    
    

    def test_remove_subdivisions(self):       
        remove_subdivisions_func = self.released_module.lab2.remove_subdivisions
        print("TEST REMOVE SUBDIVISIONS...\n")
        
        #Test with a graph we know the right answer after remove subdivisions.
        G = nx.Graph()
        [G.add_node(node) for node in range(1,10)]
        G.add_edges_from([(1,2),(2,3),(3,4),(4,5),(1,6),(6,7),(7,8),(8,9),(9,10),(5,10),(1,7),(7,3),(3,9),(9,5)])
        
        #Right answer after removing subdivisions.
        G_sol = nx.Graph()
        [G_sol.add_node(node) for node in range(1,10,2)]
        G_sol.add_edges_from([(1, 7), (1, 3), (3, 7), (3, 9), (3, 5), (5, 9), (7, 9)])
            
        #Graph after passing to the function remove sbdivisions.
        G_func = remove_subdivisions_func(G)
        expected_result = G_func.edges()
        sol_func = G_sol.edges()
        
        #print(len(G.edges()))
        #print(len(G.nodes()))
        
        #Comparation expected graph with graph after passed to function.
        print(f"The test result is (True = passed): {expected_result == sol_func}")

        
        #Test for graph size of 100 nodes (complete graph of 100 nodes).
        k100 = nx.complete_graph(100)
        expected_result = k100.copy()
        
        k100.add_node(100)
        k100.add_node(101)
        k100.add_edges_from([(99,100),(100,101)])
             
        expected_result.add_node(101)
        expected_result.add_edge(99,101)
        
        #nx.draw(G_sol)
        #plt.show()
        #print(len(k100.edges()))
        #print(len(k100.nodes()))
        
        #Comparation expected result with result provided by our function.
        sol = remove_subdivisions_func(k100)
        if (sol.edges() == expected_result.edges() and sol.nodes() == expected_result.nodes()):
            print("The test result is (True = passed): True\n\n")
        

        
    def test_contains_K5_subgraph(self):
        contains_K5_subgraph_func = self.released_module.lab2.contains_K5_subgraph
        
        #Creation of a k5 graph.
        print("TEST CONTAINS K5 SUBGRAPH...\n")
        miquel = nx.Graph()
        [miquel.add_node(node) for node in range(1,6)]
        for node1 in miquel.nodes():
            for node2 in miquel.nodes():
                if (node1 != node2):
                    miquel.add_edge(node1,node2)
        
        #print(len(miquel.edges()))
        #print(len(miquel.nodes()))
        
        expected_result1 = True
        print(f"The test result is (True = passed): {expected_result1 == contains_K5_subgraph_func(miquel)}")
        
        #Creation of a graph which has a k5 subgraph.
        oriol = nx.Graph()
        [oriol.add_node(node) for node in range(1,7)]
        for node1 in oriol.nodes():
            for node2 in oriol.nodes():
                if (node1 != node2):
                    oriol.add_edge(node1,node2)
        oriol.add_edge(7,1)
        
        #print(len(oriol.edges()))
        #print(len(oriol.nodes()))
        
        #Comparation expected result with result provided by our function.                       
        expected_result2 = True
        print(f"The test result is (True = passed): {expected_result2 == contains_K5_subgraph_func(oriol)}")
        
        
        #Using networkx generator graph.
        miguel_hernandez = nx.complete_graph(5)
        
        #print(len(miguel_hernandez.edges()))
        #print(len(miguel_hernandez.nodes()))
        
        #Comparation expected result with result provided by our function.
        expected_result3 = True
        print(f"The test result is (True = passed): {expected_result3 == contains_K5_subgraph_func(miguel_hernandez)}\n\n")
      
                

    def test_contains_K33_subgraph(self):
        print("\n______________________________________________________________________")
        print("______________________________________________________________________")
        
        print(" _______ ______  _____ _______   _               ____    ___  ")
        print("|__   __|  ____|/ ____|__   __| | |        /\   |  _ \  |__ \ ")
        print("   | |  | |__  | (___    | |    | |       /  \  | |_) |    ) |")
        print("   | |  |  __|  \___ \   | |    | |      / /\ \ |  _ <    / / ")
        print("   | |  | |____ ____) |  | |    | |____ / ____ \| |_) |  / /_ ")
        print("   |_|  |______|_____/   |_|    |______/_/    \_\____/  |____|")
        
        print("_____________________________________________________________________")
        print("_________________________________________________by: Oriol and Miquel\n\n\n")
        
        
        
        contains_K33_subgraph_func = self.released_module.lab2.contains_K33_subgraph
                         
        print("TEST CONTAINS K33 SUBGRAPH...\n")      
        #Creation of a K33 graph.
        oriol = nx.Graph()
        [oriol.add_node(node) for node in range(1,7)]
        for i in range(1,4):
            for j in range(4,7):
                oriol.add_edge(i,j)
            
        #print(len(oriol.edges()))
        #print(len(oriol.nodes()))
         
        #Comparation expected result with result provided by our function.
        expected_result3 = True
        print(f"The test result is (True = passed): {expected_result3 == contains_K33_subgraph_func(oriol)}")
                
        
        #Creation of a graph which has a k33 subgraph.
        miguel_hernandez = nx.Graph()
        [miguel_hernandez.add_node(node) for node in range(1,7)]
        for i in range(1, 4):
            for j in range(4,7):
                miguel_hernandez.add_edge(i,j)
                
        miguel_hernandez.add_node(10)
        miguel_hernandez.add_edge(10,2)
        
        #print(len(miguel_hernandez.edges()))
        #print(len(miguel_hernandez.nodes()))
        
        #Comparation expected result with result provided by our function.
        expected_result3 = True
        print(f"The test result is (True = passed): {expected_result3 == contains_K33_subgraph_func(miguel_hernandez)}")
        
        
        #Creation of a non-K33 contained subraph.
        #K5 graph below.
        miquel = nx.Graph()
        [miquel.add_node(node) for node in range(1,6)]
        for node1 in miquel.nodes():
            for node2 in miquel.nodes():
                if (node1 != node2):
                    miquel.add_edge(node1,node2)
        
        #print(len(miquel.edges()))
        #print(len(miquel.nodes()))
        
        #Comparation expected result with result provided by our function.
        expected_result4 = False
        print(f"The test result is (True = passed): {expected_result4 == contains_K33_subgraph_func(miquel)}")
        
        #Using networkx generator graph.
        oriol_and_mike = nx.complete_graph(6)
        
        #print(len(oriol_and_mike.edges()))
        #print(len(oriol_and_mike.nodes()))
        
        #Comparation expected result with result provided by our function.
        expected_result5 = False
        print(f"The test result is (True = passed): {expected_result5 == contains_K33_subgraph_func(oriol_and_mike)}\n\n")
      
            

if __name__ == '__main__':
    sys.argv = sys.argv[0:1] + [arg for arg in sys.argv if arg == "-v"]
    unittest.main()

