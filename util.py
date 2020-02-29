"""
Some utility functions used in several modules but not really related to any of them.
"""

import logging
import networkx as nx
import random

META_PREFIX = '#'


def add_weights(in_path: str, smallest_weight: int, largest_weight: int, out_path: str):
    """
    Gets a path of a network file (a file that contains the edges of the networks, things like:
    #from  to
     1     0
     1     2
     ...)
     and creates a file describing the same network, but with weights and no "headers" (metadata lines that starts with
     #). The weights are randomly chosen within a given range.

     Output Example:
     1  0   11
     1  2   5
     ...
    :param in_path: an unweighted network file path.
    :param smallest_weight: The smallest weight in the range.
    :param largest_weight: The largest weight in the range.
    :param out_path: the path of the wanted output file.
    """
    print("Adding weights...")
    with open(out_path, 'w') as weighted_net:
        with open(in_path, 'r') as original_net:
            for line in original_net:
                if not line.startswith(META_PREFIX):
                    weight = random.randint(smallest_weight, largest_weight)
                    weighted_net.write(line.rstrip('\n') + "\t" + str(weight) + '\n')


def generate_graph(weighted_net_path: str) -> nx.DiGraph:
    """
    Converts the file in weighted_net_path into a NetworkX directed graph object.
    :param weighted_net_path: the path of the weighted network to be converted into a nx graph.
    """
    logging.info("Generating network graph...")
    net_graph = nx.read_edgelist(weighted_net_path, nodetype=int,
                                 data=(('weight', float),), create_using=nx.DiGraph())
    return net_graph

