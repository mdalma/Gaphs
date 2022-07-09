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

from test_lab import TestLab
import renfe


class TestLab1(TestLab, unittest.TestCase):
    name = "lab1"

    def test_components_are_complete(self):
        """Verify that each node is in exactly one component among the list
        returned by the submitted solution.

        Note: This function does NOT check all conditions described
        in the assignment.
        """
        print("\nInitializing test environment...")
        self.reader = renfe.RenfeReader(prebuilt_dir=os.path.dirname(__file__))
        self.stations_by_id = self.reader.get_stations_by_id()
        self.journeys = self.reader.get_journeys()
        print("... initialized!")

        network_list = [sorted(self.stations_by_id[id] for id in l)
                        for l in sorted(self.released_module.lab1.get_network_list(),
                                        key=len, reverse=True)]
        for station in self.stations_by_id.values():
            belongs_to = sum(1 if station in component else 0
                             for component in network_list)
            assert belongs_to == 1, (station, belongs_to)

        assert False




    #Provided in test_lab0.
    def test_create_station_graph(self):
        G = self.released_module.lab1.create_station_graph()
        assert sum(G.edges[e]["count"] for e in G.edges) == 45825, \
            f"Are you counting every trip correctly?"
        reader = renfe.RenfeReader()
        stations_by_id = reader.get_stations_by_id()
        station_uab = stations_by_id['72503']
        station_cerdanyola = stations_by_id['78706']
        station_sant_cugat = stations_by_id['72502']
        assert G.edges[station_uab, station_cerdanyola]["count"] == 67
        assert G.edges[station_sant_cugat, station_uab]["count"] == 32
     
          
    def test_get_network_list(self):
        grapher = renfe.RenfeBasicGrapher()
        G = grapher.get_networkx_graph() 

        networks = self.released_module.lab1.get_network_list()
        
        assert (nx.number_connected_components(G)) == len(networks), "NOT OK"
        print("OK")
        
    
    def test_get_time_graph(self):
        grapher = renfe.RenfeBasicGrapher()
        G = grapher.get_networkx_graph() 
               
        assert G.size(['weight']) / G.size() == self.released_module.lab1.get_time_graph(), "NOT OK"
        print("OK")
        
  
    def test_plan_route(self, station_a, station_b):
        grapher = renfe.RenfeBasicGrapher()
        G = grapher.get_networkx_graph() 
        
        if nx.dijkstra_path(G, station_a, station_b) == 'NetworkXNoPath':
            if ( self.released_module.lab1.plan_route(G, station_a, station_b) == [] ):
                print("OK")
            else:
                print("NOT OK")
        else:
            path_sol, lenght_path_sol = nx.dijkstra_path(G, station_a, station_b), nx.shortest_path_length(G, station_a, station_b) 
            path, length_path = self.released_module.lab1.plan_route(G, station_a, station_b)
            if (path_sol == path and lenght_path_sol == length_path):
                print("OK")
            else:
                print("NOT OK")



if __name__ == '__main__':
    sys.argv = sys.argv[0:1] + [arg for arg in sys.argv if arg == "-v"]
    unittest.main()
