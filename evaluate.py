import random
from Problems.ShortestPaths.Graph import Graph

NETWORK_PATH = 'Networks\web-Stanford.txt'
WEIGHTED_NET_FILE_NAME = 'weighted_net.txt'


def add_weights(net_path: str, smallest_weight: int, largest_weight: int):
    with open(WEIGHTED_NET_FILE_NAME, 'w') as weighted_net:
        with open(net_path, 'r') as original_net:
            for line in original_net:
                if not line.startswith('#'):
                    weight = random.randint(smallest_weight, largest_weight)
                    weighted_net.write(line.rstrip('\n') + "\t" + str(weight) + '\n')


def generate_graph() -> Graph:
    net_graph = Graph()
    with open(WEIGHTED_NET_FILE_NAME, 'r') as network_file:
        for line in network_file:
            line_data = line.rstrip('\n').split("\t")
            net_graph.add_edge(line_data[0], line_data[1], line_data[2])
    return net_graph


if __name__ == '__main__':
    add_weights(NETWORK_PATH, 2, 10)
    graph = generate_graph()
    # add weights if needed
    # generate graph objects
    # apply algorithms on the network
    # write logs to file: paths discovered, score, I, E etc.
    # measure time, diversification and paths length.
    # print results.
    # delete helper files etc.
    pass
