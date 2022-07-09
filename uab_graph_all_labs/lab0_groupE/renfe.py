# -*- coding: utf8 -*-
"""
:: Labs of Graphs, Topology, and Discrete Geometry - Data Engineering, UAB - 2019/2020 ::

Module to process Renfe's output raw data.

The Station, Advance and Journey classes model different aspects of trains and their behavior.

The RenfeReader class provides a list of all found stations in get_stations_by_id(),
and a list of all train journeys (from beginning to end of a line) with get_journeys().

New classes defined to create graphs must subclass RenfeReader, see RenfeBasicGrapher for an example.

The plot_station_graph is provided as an example of how to plot graphs in networkx.

Additional information:
    - see https://networkx.github.io/documentation/stable/tutorial.html for a tutorial on networkx
    - see https://docs.python.org/3/tutorial/introduction.html for a basic introduction to Python
"""

import os
import copy

try:
    import numpy as np
except ImportError as ex:
    raise ImportError("Numpy library not found. Try:\npip3 install numpy") from ex
try:
    import pandas as pd
except ImportError as ex:
    raise ImportError("Pandas library not found. Try:\npip3 install pandas") from ex
try:
    import networkx as nx
except ImportError as ex:
    raise ImportError("networkx library not found. Try:\npip3 install --user networkx")

try:
    from matplotlib import pyplot as plt
except ImportError as ex:
    raise ImportError("matplotlib library not found. Try:\npip3 install --user matplotlib")

import config
from config import options


def text_to_label(s):
    return s.strip().title()


def clean_journey_name(stop_name):
    while "  " in stop_name:
        stop_name = stop_name.replace("  ", " ")
    return " - ".join(s.strip() for s in stop_name.split("-")).strip()


class Station:
    """A train station
    """

    def __init__(self, id: str, name: str, latitude: float, longitude: float, is_cercanias: bool):
        """
        :param id: unique id for the station
        :param name: station's long name
        :param latitude: physical latitude point
        :param longitude: physical longitude point
        :param is_cercanias: is this a Cercanías stop?
        """
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.is_cercanias = is_cercanias

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"[{type(self).__name__}:{self.id}:{self.name}@{self.latitude},{self.longitude}]"

    def __eq__(self, other):
        try:
            return other.id == self.id
        except AttributeError:
            return False

    def __gt__(self, other):
        try:
            return self.id > other.id
        except AttributeError:
            return False

    def __lt__(self, other):
        try:
            return self.id < other.id
        except AttributeError:
            return False

    def __hash__(self):
        return self.id.__hash__()


class Advance:
    """A train advancing from one station to the next at a given time of the day
    """

    def __init__(self, station_start: Station, station_end: Station, start_time_s: int, end_time_s: int):
        """
        :param station_start: the train starts at this station
        :param station_end: the train ends at this station
        :param start_time_s: departure time, expressed in seconds since last midnight
        :param end_time_s: arrival time, expressed in seconds since last midnight
        """
        self.station_start = station_start
        self.station_end = station_end
        self.start_time_s = start_time_s
        self.end_time_s = end_time_s
        assert self.start_time_s < self.end_time_s
        assert self.station_start != self.station_end

    def __str__(self):
        return f"[{type(self).__name__}:{self.station_start}({self.station_start.id})@{self.start_time_s:.3f}s" \
               f"->{self.station_end}({self.station_end.id})@{self.end_time_s:.3f}s]"


class Journey:
    """The journey of a single train through different stops.
    """

    def __init__(self, id: str, name: str, advances=[]):
        """
        :param id: unique identifier for a Journey
        :param name: name describing the Journey (e.g., train line + direction)
        :param advances: initial list of Advance instances describing the journey,
          can be expanded with self.add_advance
        """
        self.id = id
        self.name = name
        self.advances = []
        for adv in advances:
            self.add_advance(adv)

    def add_advance(self, advance: Advance):
        """Add the next train advance of this journey
        """
        if self.advances:
            if advance.station_start != self.advances[-1].station_end:
                raise ValueError(f"The new advance={advance} has departing station {advance.station_start} "
                                 f"but the current journey was at {self.advances[-1].station_end}")
            if advance.start_time_s < self.advances[-1].end_time_s:
                raise ValueError(f"The new advance={advance} has departing time {advance.start_time_s} "
                                 f"but the current journey arrived at {self.advances[-1].end_time_s}")
        self.advances.append(advance)

    def __str__(self):
        return f"[{type(self).__name__}:{self.id}:{self.name}:({len(self.advances)} advances)]"


class RenfeReader:
    """Reader of Renfe's CSV database dump.
    """
    # Caching variables
    _journeys_by_day = {}
    _train_times_df = None

    def __init__(self, prebuilt_dir=None):
        self.prebuilt_dir = prebuilt_dir
        self.stops_df = self.read_stops()
        self.services_df = self.read_services()
        self.routes_df = self.read_routes()
        self.trips_df = self.read_trips()
        self.train_times_df = self.read_train_times()
        self.stations_by_id = self.get_stations_by_id()

    def get_stations_by_id(self):
        """Return a list of Station instances indexed id
        """
        stations = set()
        for stop in self.stops_df.itertuples():
            new_station = Station(
                id=stop.stop_id, name=stop.stop_name,
                latitude=stop.stop_lat, longitude=stop.stop_lon,
                is_cercanias=stop.stop_is_cercanias)
            stations.add(new_station)
        return {s.id: s for s in stations}

    def get_journeys(self, target_day=config.example_day):
        """Get a list of all Journeys
        (for the target_day only if self.target_day is not None)
        """
        try:
            return copy.deepcopy(self._journeys_by_day[target_day])
        except KeyError:
            pass

        journeys = []
        joint_df = self.get_joint_df(target_date=target_day)
        for route_id, route_df in joint_df.groupby("route_id"):
            route_name = route_df.iloc[0].route_name.replace(chr(0xa6), "ñ")
            if options.verbose > 1:
                print(f"Processing route {route_name}...")

            for trip_id, trip_df in route_df.groupby("trip_id"):
                new_journey = Journey(id=trip_id, name=route_name)
                trip_df = trip_df.sort_values(by="stop_sequence")
                prev_stop = None
                for stop in trip_df.itertuples():
                    if prev_stop is None:
                        prev_stop = stop
                        continue

                    try:
                        new_journey.add_advance(Advance(
                            station_start=self.stations_by_id[prev_stop.stop_id],
                            station_end=self.stations_by_id[stop.stop_id],
                            start_time_s=prev_stop.arrival_seconds,
                            end_time_s=stop.arrival_seconds))
                    except KeyError as ex:
                        print("[watch] prev_stop = {}".format(prev_stop))
                        raise ex

                    prev_stop = stop
                journeys.append(new_journey)
        RenfeReader._journeys_by_day[target_day] = journeys
        return journeys

    def get_joint_df(self, target_date=None):
        if options.verbose > 1:
            print("Generating joint dataframe...")

        # Read all trip metainformation
        joint_df = self.services_df.join(
            self.trips_df.set_index("service_id", drop=False), on="service_id")
        joint_df = joint_df.set_index("route_id").join(
            self.routes_df.set_index("route_id", drop=False), on="route_id")
        for c in joint_df.columns:
            missing_indices = joint_df[c].isnull()
            joint_df.loc[missing_indices, c] = f"Unknown (service " \
                                               + joint_df.loc[missing_indices, "service_id"] \
                                               + ")"

        joint_df = joint_df.set_index("trip_id").join(
            self.trips_df.set_index("trip_id"), on="trip_id", rsuffix="_repeated")
        joint_df = joint_df.loc[:, [c for c in joint_df.columns if not c.endswith("_repeated")]]

        # Filter by target date
        if target_date is not None:
            joint_df = joint_df[joint_df["start_date"] == target_date]
            if len(joint_df) == 0:
                raise ValueError(f"No results found for {target_date}")

        # Load train times for the selected trips
        joint_df = joint_df.join(self.train_times_df.set_index("trip_id"), on="trip_id", how="inner")
        if options.verbose > 1:
            print(f"Read {len(joint_df)} train times for " +
                  (target_date if target_date is not None else "all dates"))
        joint_df.loc[:, "stop_id"] = joint_df["stop_id"].astype(str)

        for c in joint_df.columns:
            if joint_df[c].isna().any():
                print(f"{c} has na values")

        assert not self.train_times_df.isna().any().any()
        for c in self.train_times_df.columns:
            if self.train_times_df[c].isna().any():
                print(f"{c} has na values (train_times)")

        assert not joint_df.isna().any().any()

        return joint_df

    def read_stops(self):
        """Read the stops.txt csv data
        """
        all_stops = pd.read_csv(
            config.stops_full_csv_path,
            sep=";",
            encoding="utf8",
            converters={
                " CÓDIGO": str,
                "DESCRIPCION": text_to_label,
                "LATITUD": float,
                "LONGITUD": float,
                "DIRECCIÓN": text_to_label,
                "C.P.": str.strip,
                "POBLACION": text_to_label,
                "PROVINCIA": text_to_label,
                "PAIS": text_to_label,
                "CERCANIAS": lambda s: s.strip() == "YES",
                "FEVE": lambda s: s == "YES"})
        # Rename column names
        for old, new in {" CÓDIGO": "stop_id",
                         "DESCRIPCION": "stop_name",
                         "LATITUD": "stop_lat",
                         "LONGITUD": "stop_lon",
                         "DIRECCIÓN": "stop_address",
                         "C.P.": "stop_cp",
                         "POBLACION": "stop_city",
                         "PROVINCIA": "stop_province",
                         "PAIS": "stop_country",
                         "CERCANIAS": "stop_is_cercanias",
                         "FEVE": "stop_is_feve"}.items():
            all_stops.columns = all_stops.columns.str.replace(old, new)

        partial_df = pd.read_csv(config.stops_partial_csv_path,
                                 converters={"stop_lat": float,
                                             "stop_lon": float,
                                             "stop_name": str,
                                             "stop_id": str.strip},
                                 encoding="utf8")
        partial_df.loc[:, "stop_is_cercanias"] = True
        all_stops = all_stops.append(partial_df, sort=False)

        assert not any(all_stops[c].isnull().any()
                       for c in all_stops.columns
                       if c not in ["stop_address", "stop_city", "stop_country",
                                    "stop_cp", "stop_is_feve", "stop_province"])
        assert not all_stops["stop_id"].isnull().any()
        all_stops.sort_values(by="stop_id", inplace=True)

        return all_stops

    def read_services(self):
        """Read Renfe's list of services in CSV format
        """
        if options.verbose > 1:
            print(f"Reading {os.path.basename(config.services_csv_path)}...")

        df = pd.read_csv(
            config.services_csv_path,
            index_col="service_id",
            converters={"service_id": str.strip,
                        "monday": int,
                        "tuesday": int,
                        "wednesday": int,
                        "thursday": int,
                        "friday": int,
                        "saturday": int,
                        "sunday": int,
                        "start_date": str,
                        "end_date": str,
                        },
            encoding="utf8")
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            df[day] = df[day].apply(lambda v: v != 0)

        return df

    def read_routes(self):
        if options.verbose > 1:
            print(f"Reading {os.path.basename(config.routes_csv_path)}...")

        df = pd.read_csv(
            config.routes_csv_path,
            converters={"route_id": str.strip,
                        "route_short_name": str.strip,
                        "route_long_name": str.strip},
            encoding="utf8")

        df.loc[:, "route_long_name"] = df["route_long_name"].apply(clean_journey_name)
        df.loc[:, "route_name"] = df.loc[:, "route_short_name"] + ": " + df.loc[:, "route_long_name"]

        return df

    def read_trips(self):
        if options.verbose > 1:
            print(f"Reading {os.path.basename(config.trips_csv_path)}...")

        return pd.read_csv(config.trips_csv_path,
                           converters={"route_id": str.strip,
                                       "service_id": str.strip,
                                       "trip_id": str.strip,
                                       "trip_headsign": str},
                           encoding="utf8")

    def read_train_times(self):
        if self._train_times_df is not None:
            return self._train_times_df.copy()

        if options.verbose > 1:
            print(f"Reading {os.path.basename(config.times_csv_path)}...")

        train_times_df = pd.read_csv(config.times_csv_path,
                                     converters={"trip_id": str.strip,
                                                 "arrival_time": str,
                                                 "departure_time": str,
                                                 "stop_id": str,
                                                 "stop_sequence": int
                                                 },
                                     encoding="utf8")
        train_times_df[["arrival_hour", "arrival_minute", "arrival_second"]] = \
            train_times_df["arrival_time"].str.split(":", expand=True).astype(int)
        train_times_df[["departure_hour", "departure_minute", "departure_second"]] = \
            train_times_df["departure_time"].str.split(":", expand=True).astype(int)
        train_times_df["arrival_seconds"] = train_times_df["arrival_hour"] * 60 * 60 \
                                            + train_times_df["arrival_minute"] * 60 \
                                            + train_times_df["arrival_second"]
        train_times_df["departure_seconds"] = train_times_df["departure_hour"] * 60 * 60 \
                                              + train_times_df["departure_minute"] * 60 \
                                              + train_times_df["departure_second"]

        train_times_df["arrival_seconds"] = train_times_df["arrival_seconds"].astype(int)
        train_times_df["departure_seconds"] = train_times_df["departure_seconds"].astype(int)
        train_times_df["stop_sequence"] = train_times_df["stop_sequence"].astype(int)

        RenfeReader._train_times_df = train_times_df
        return train_times_df


class RenfeGrapher(RenfeReader):
    """Base class for Renfe graphers
    """
    def get_networkx_graph(self, target_day=config.example_day):
        raise NotImplementedError("Subclasses must implement this function")


class RenfeBasicGrapher(RenfeGrapher):
    """
    Example, basic class to create representations of Renfe's cercanías' trains.

    Each station is a node. Two stations have an edge if there is at least
    one train that passes by both of them.
    """

    def get_networkx_graph(self, target_day=config.example_day):
        """
        Get a symmetric graph of Stations, connected whenever at least one
        advance is defined in Renfe's DB between the two stations.
        :param target_day: if provided, DB is only queried that day
        :return: a symmetric graph of Station instances
        """
        # New, empty graph
        G = nx.Graph()

        # Add stations as nodes
        station_list = [s for s in self.stations_by_id.values()]
        for station in station_list:
            G.add_node(station)

        # For each train advance (movement from station A to B), add an edge between A and B
        journeys = self.get_journeys(target_day=target_day)
        for journey in journeys:
            for advance in journey.advances:
                if not G.has_edge(advance.station_start, advance.station_end):
                    # Multiple journeys cover any two pairs of stations
                    G.add_edge(advance.station_start, advance.station_end)
        return G


def plot_station_graph(G, output_path=None):
    """Plot and show a graph of Stations
    :param G: graph to plot
    :param output_path: if None, graph is shown after rendering. If not none,
      it is the path where the plot is to be saved
    """
    plt.figure()
    nx.draw_networkx(
        G,
        pos={n: (n.longitude, n.latitude) for n in G.nodes},
        node_size=0.5,
        with_labels=False)
    plt.axis("off")
    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()
    plt.close()
