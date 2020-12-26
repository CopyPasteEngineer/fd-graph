import yaml
import numpy as np

from .graphic import GraphicScreen
from .graph import Graph
from . import config


class Game:
    def __init__(self, config_file):
        with open(config_file) as file:
            params = yaml.load(file, Loader=yaml.FullLoader)
        config.set(**params)

    def start(self):
        width, height = config.get('game.width'), config.get('game.height')
        n_nodes = config.get('graph.node.maxCount')
        n_edges = config.get('graph.edge.maxCount')
        random_seed = config.get('game.randomSeed')

        np.random.seed(random_seed)

        screen = GraphicScreen(width, height)

        graph = Graph(width, height)
        for i, j in np.random.randint(0, n_nodes, (n_edges, 2)):
            if i == j:
                continue
            graph.add_edge(i, j)
        screen.add_object(graph)

        screen.start()
