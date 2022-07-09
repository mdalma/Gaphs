#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:27:14 2020

@author: miquel

'X' IS THE INPUT SIZE, THE PARAMETER THAT WILL BE PASSED TO OUR FUNCTIONS.
'Y' IS THE TIME THAT OUR FUNCTIONS NEED TO PROCESS THE INPUT PARAMETER (DEPENDING OF THE SIZE)

WITH THE RESULTS, WE CAN MAKE A GRAFIC AND ANALIZE THE CURVE OF IT.
AFFORTUNATELY, WE WOULD ESTTIMATE THE COMPLEXITY OF THE FUNCTIONS...


"""







"""
import itertools
import networkx as nx
from time import time
from lab2 import remove_subdivisions, contains_K5_subgraph, contains_K33_subgraph


#REMOVE SUBDIVISIONS ESTIMATION
k50 = nx.complete_graph(50)
k50.add_node(50)
k50.add_node(51)
k50.add_edges_from([(49,50),(50,51)])
start_time = time()
G = remove_subdivisions(k50)
y1 = time() - start_time
print(f"Input (x = 50), Time (y = {y1})")

k100 = nx.complete_graph(100)
k100.add_node(100)
k100.add_node(101)
k100.add_edges_from([(99,100),(100,101)])
start_time = time()
G = remove_subdivisions(k100)
y2 = time() - start_time
print(f"Input (x = 100), Time (y = {y2})")

k150 = nx.complete_graph(150)
k150.add_node(150)
k150.add_node(151)
k150.add_edges_from([(149,150),(150,151)])
start_time = time()
G = remove_subdivisions(k150)
y3 = time() - start_time
print(f"Input (x = 150), Time (y = {y3})")

k200 = nx.complete_graph(200)
k200.add_node(200)
k200.add_node(201)
k200.add_edges_from([(199,200),(200,201)])
start_time = time()
G = remove_subdivisions(k200)
y4 = time() - start_time
print(f"Input (x = 200), Time (y = {y4})")

k250 = nx.complete_graph(250)
k250.add_node(250)
k250.add_node(251)
k250.add_edges_from([(249,250),(250,251)])
start_time = time()
G = remove_subdivisions(k250)
y5 = time() - start_time
print(f"Input (x = 250), Time (y = {y5})")

k300 = nx.complete_graph(300)
k300.add_node(300)
k300.add_node(301)
k300.add_edges_from([(299,300),(300,301)])
start_time = time()
G = remove_subdivisions(k300)
y6 = time() - start_time
print(f"Input (x = 300), Time (y = {y6})")

k400 = nx.complete_graph(400)
k400.add_node(400)
k400.add_node(401)
k400.add_edges_from([(399,400),(400,401)])
start_time = time()
G = remove_subdivisions(k400)
y7 = time() - start_time
print(f"Input (x = 400), Time (y = {y7})")

k500 = nx.complete_graph(500)
k500.add_node(500)
k500.add_node(501)
k500.add_edges_from([(499,500),(500,501)])
start_time = time()
G = remove_subdivisions(k500)
y8 = time() - start_time
print(f"Input (x = 500), Time (y = {y8})")

k750 = nx.complete_graph(750)
k750.add_node(750)
k750.add_node(751)
k750.add_edges_from([(749,750),(750,751)])
start_time = time()
G = remove_subdivisions(k750)
y9 = time() - start_time
print(f"Input (x = 750), Time (y = {y9})")

k1000 = nx.complete_graph(1000)
k1000.add_node(1000)
k1000.add_node(1001)
k1000.add_edges_from([(999,1000),(1000,1001)])
start_time = time()
G = remove_subdivisions(k1000)
y10 = time() - start_time
print(f"Input (x = 1000), Time (y = {y10})")

k1500 = nx.complete_graph(1500)
k1500.add_node(1500)
k1500.add_node(1501)
k1500.add_edges_from([(1499,1500),(1500,1501)])
start_time = time()
G = remove_subdivisions(k1500)
y11 = time() - start_time
print(f"Input (x = 1500), Time (y = {y11})")

k2000 = nx.complete_graph(2000)
k2000.add_node(2000)
k2000.add_node(2001)
k2000.add_edges_from([(1999, 2000),(2000,2001)])
start_time = time()
G = remove_subdivisions(k2000)
y12 = time() - start_time
print(f"Input (x = 2000), Time (y = {y12})")

k2500 = nx.complete_graph(2500)
k2500.add_node(2500)
k2500.add_node(2501)
k2500.add_edges_from([(2499, 2500),(2500,2501)])
start_time = time()
G = remove_subdivisions(k2500)
y13 = time() - start_time
print(f"Input (x = 2500), Time (y = {y13})")


#CONTAINS K5 SUBGRAPH ESTIMATION
start_time = time()
contains_K5_subgraph(nx.complete_graph(5))
y = time() - start_time
print(f"Input (x = 5), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(10))
y = time() - start_time
print(f"Input (x = 10), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(15))
y = time() - start_time
print(f"Input (x = 15), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(20))
y = time() - start_time
print(f"Input (x = 20), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(25))
y = time() - start_time
print(f"Input (x = 25), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(40))
y = time() - start_time
print(f"Input (x = 40), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(60))
y = time() - start_time
print(f"Input (x = 60), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(100))
y = time() - start_time
print(f"Input (x = 100), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(200))
y = time() - start_time
print(f"Input (x = 200), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(400))
y = time() - start_time
print(f"Input (x = 400), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(1000))
y = time() - start_time
print(f"Input (x = 1000), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(2000))
y = time() - start_time
print(f"Input (x = 2000), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(3000))
y = time() - start_time
print(f"Input (x = 3000), Time (y = {y})")

start_time = time()
contains_K5_subgraph(nx.complete_graph(4000))
y = time() - start_time
print(f"Input (x = 4000), Time (y = {y})")

"""






