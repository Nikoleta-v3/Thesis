"""
A script to generate the co authorship network. Uses articles' meta data, in the
format of `arcas` result, and then uses `networkx` to construct the network.

Each node is an individual author, and a edge represents whether two authors
have published together.
"""
from importlib.machinery import SourceFileLoader
import sys

import numpy as np
import pandas as pd

import networkx as nx

tools = SourceFileLoader("tools", "src/tools.py").load_module()


if __name__ == "__main__":

    directory = sys.argv[1]

    ipd = pd.read_json("%s/pd_November_2018_clean.json" % directory)
    anarchy = pd.read_json("%s/anarchy_November_2018_clean.json" % directory)
    auction = pd.read_json("%s/auction_November_2018_clean.json" % directory)

    dataframes, topics = [ipd, auction, anarchy], ["pd", "auction", "anarchy"]
    output_location = "%s/networks/" % directory

    print("Constructing networks")
    for data, topic in zip(dataframes, topics):
        graph = tools.generate_co_authorship_graph(data)
        nx.write_gml(graph, "{}{}_graph.gml".format(output_location, topic))

    for data, topic in zip(dataframes, topics):
        periods = np.sort(data["date"].unique())
        periods = periods[~np.isnan(periods)]
        periods = periods[1:]
        cumulative_dataframes = [
            data[data["date"] <= period].reset_index() for period in periods
        ]

        for i, frame in enumerate(cumulative_dataframes):
            graph = tools.generate_co_authorship_graph(frame)
            nx.write_gml(
                graph, "{}G_{}_{}.gml".format(output_location, topic, i)
            )
    print("Finish")
