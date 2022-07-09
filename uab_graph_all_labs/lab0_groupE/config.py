#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:: Labs of Graphs, Topology, and Discrete Geometry - Data Engineering, UAB - 2019/2020 ::

General configuration and CLI options
"""

import os
import argparse
import datetime

parser = argparse.ArgumentParser(description="")
parser.add_argument("-v", "--verbose", help="Be verbose? Repeat for more", action="count", default=0)
options = parser.parse_known_args()[0]

data_dir = os.path.join(os.path.dirname(__file__), "data")
assert os.path.isdir(data_dir)

stops_full_csv_path = os.path.join(data_dir, "listado-estaciones-completo.csv")
assert os.path.exists(stops_full_csv_path), stops_full_csv_path
stops_partial_csv_path = os.path.join(data_dir, "stops.txt")
assert os.path.exists(stops_full_csv_path), stops_full_csv_path
services_csv_path = os.path.join(data_dir, "calendar.txt")
assert os.path.exists(services_csv_path), services_csv_path
routes_csv_path = os.path.join(data_dir, "routes.txt")
assert os.path.exists(routes_csv_path), routes_csv_path
trips_csv_path = os.path.join(data_dir, "trips.txt")
assert os.path.exists(trips_csv_path), trips_csv_path
times_csv_path = os.path.join(data_dir, "stop_times.txt")
assert os.path.exists(times_csv_path), times_csv_path

example_day = "20191118"
