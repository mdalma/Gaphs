#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:: Labs of Graphs, Topology, and Discrete Geometry - Data Engineering, UAB - 2019/2020 ::

Template for Lab1's tasks. See the assignment for details.

IMPORTANT: Don't change the provided function names, parameters or expected return.
"""

import networkx as nx
#COLLECTIONS --> This module implements specialized container datatypes (ex: fast appends and leftpops).
import collections   
import renfe
#OPERATOR --> Sort the values of a dictionary (for Dijkstra algorithm).
import operator


def create_station_graph():
    G = nx.Graph()
    reader = renfe.RenfeReader()
    stations_by_id = reader.get_stations_by_id()

    journeys = reader.get_journeys()    
    [G.add_node(x) for x in stations_by_id.values()]

    for rutas in journeys:
	    advance = rutas.advances
	    for estacio in advance:
		    if not G.has_edge(estacio.station_start, estacio.station_end):
			    G.add_edge(estacio.station_start, estacio.station_end)
			    G.edges[estacio.station_start, estacio.station_end]['count'] = 1
		    else:
			    G.edges[estacio.station_start, estacio.station_end]['count'] += 1
				
    return G


def bfs(origen,G):
    pendents = collections.deque()
    visitats = collections.deque()

    pendents.append(origen)
    while len(pendents) != 0:
        visitat = pendents.popleft()
        visitats.append(visitat)
        for veins in G.neighbors(visitat):
            if veins not in visitats and veins not in pendents:
                pendents.append(veins)
                             
    return visitats
   
    
def get_network_list():
    G = create_station_graph()
    networks = []   
    for node in G.nodes():
            nodes_network = bfs(node,G)
            #Sorted --> Control d'errors (per si hi han dos nodes que pertanyen al mateixa network.)
            if sorted(nodes_network) not in networks:
                networks.append(nodes_network)
            else:
                pass
    
    return networks

"""
xarxes = get_network_list()
minim = min(xarxes)
maxim = max(xarxes)
print(f"Min : {len(minim)}\nMax: {len(maxim)}\nTotal Network : {len(xarxes)}")
"""

def get_time_graph():
    G = nx.Graph()
    reader = renfe.RenfeReader()
    stations_by_id = reader.get_stations_by_id()

    journeys = reader.get_journeys()    
    [G.add_node(x) for x in stations_by_id.values()]

    journeys = reader.get_journeys()
    for journey in journeys:
        for advance in journey.advances:
            if G.has_edge(advance.station_start, advance.station_end) == True:
                G.edges[advance.station_start, advance.station_end]['count'] += 1
                #This weight is not the averge
                G.edges[advance.station_start, advance.station_end]['weight'] +=  (advance.end_time_s - advance.start_time_s)
            else:
                #Directed edge.
                G.add_edge(advance.station_start, advance.station_end, count = 1)
                G.add_edge(advance.station_start, advance.station_end, weight = (advance.end_time_s - advance.start_time_s))
            
        for edge in G.edges():
            mitjana = (G.edges[edge]['weight'] / G.edges[edge]['count']) 
            G.edges[edge]['weight'] = mitjana

    return G

"""
G = get_time_graph()
maximo = 0
minim = float('inf')
for edge in G.edges():
    if G.edges[edge]['weight'] > maximo:
        maximo = G.edges[edge]['weight']
    if G.edges[edge]['weight'] < minim:
        minim = G.edges[edge]['weight']

print(maximo)
print(minim)
"""


#No acabat
def plan_route(G, station_a, station_b):
    priority_queue = dict()
    path = dict()
    
    #Inicialitzem. Source_node = 0. All_others = infinit.
    for node in G.nodes():
        if node == station_a:
            priority_queue[node] = 0
        else:
            priority_queue[node] = float('inf')
        
    while len(priority_queue) > 0 :         
            #Ordenar diccionary values de petit a gran (List with tupplas).
            priority_queue = sorted(priority_queue.items(), key = operator.itemgetter(1))
            #Lowest tuppla value.
            selected_node = priority_queue[0]
            #Lowest node weight.
            selected_node = selected_node[0]
            
            for vei in G.neighbors(selected_node):
                if priority_queue[vei] > priority_queue[selected_node] + G.edges[selected_node, vei]['weight']:                       
                    priority_queue[vei] = G.edges[selected_node, vei]['weight'] +  priority_queue[selected_node]
                    path[vei.id] = selected_node
                    
                    if vei.id == station_b:
                         return path
                else:
                    pass
    
    return []

"""
path = plan_route(create_station_graph(), '72503', '79404')
print(path)
"""











