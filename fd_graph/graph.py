from typing import Dict, Set, Tuple
import pygame
import numpy as np

from .graphic import GraphicObject
from . import config


class Node(GraphicObject):
    def __init__(self, n, x, y):
        self.n = n

        self.pos = np.array([x, y], dtype=float)

        if config.get('graph.node.velocity'):
            self.vel = np.random.rand(2)*10 - 5  # [-5, 5)
        else:
            self.vel = np.array([0, 0], dtype=float)

    def update(self):
        self.pos += self.vel

        if config.get('forces.viscosity.active'):
            self.vel *= config.get('forces.viscosity.constant')

    def draw(self, screen):
        color = config.get('graph.node.color')
        radius = config.get('graph.node.radius')
        pygame.draw.circle(screen, color, self.get_pos(), radius)

    def get_pos(self):
        return self.pos.round()


class Graph(GraphicObject):
    def __init__(self, screen_width, screen_height):
        self.screen_width, self.screen_height = screen_width, screen_height

        self.nodes = dict()  # type: Dict[int, Node]
        self.edges = set()  # type: Set[Tuple[int]]

    def _create_node(self, i):
        x = np.random.randint(self.screen_width*0.10, self.screen_width*0.90)
        y = np.random.randint(self.screen_height*0.10, self.screen_height*0.90)

        return Node(i, x, y)

    def add_edge(self, i: int, j: int):
        a, b = map(self._create_node, (i, j))

        self.nodes[i] = a
        self.nodes[j] = b

        edge = tuple(sorted((i, j)))
        self.edges.add(edge)

    def _apply_spring_force(self):
        k = config.get('forces.spring.constant')
        r = config.get('forces.spring.length')

        for edge in self.edges:
            a, b = map(self.nodes.get, edge)
            d = b.pos - a.pos

            size = (d**2).sum() ** 0.5  # distance from a to b

            if size == 0:  # random some small vector
                d = np.random.rand(2)
                size = (d**2).sum() ** 0.5

            unit = d / size

            force = k * (r-size) * unit
            force = np.clip(force, -5, 5)

            a.vel -= force
            b.vel += force

    def _center_nodes(self):
        center = np.zeros(2, dtype=float)

        for node in self.nodes.values():
            center += node.pos

        center /= len(self.nodes)

        center -= np.array([self.screen_width, self.screen_height])/2

        for node in self.nodes.values():
            node.pos -= center

    def _apply_electric_force(self):
        k = config.get('forces.electric.constant')
        nodes = list(self.nodes.values())

        for i, a in enumerate(nodes):
            for b in nodes[i+1:]:
                d = b.pos - a.pos

                size = (d ** 2).sum() ** 0.5  # distance from a to b

                if size > 200:
                    continue

                if size == 0:  # random some small vector
                    d = np.random.rand(2)
                    size = (d ** 2).sum() ** 0.5

                unit = d / size

                force = k/(size**2) * unit
                force = np.clip(force, -10, 10)

                a.vel -= force
                b.vel += force

    def update(self):
        if config.get('forces.spring.active'):
            self._apply_spring_force()
        if config.get('forces.electric.active'):
            self._apply_electric_force()

        for node in self.nodes.values():
            node.update()

        self._center_nodes()

    def draw(self, screen):
        self._draw_edges(screen)
        self._draw_nodes(screen)

    def _draw_edges(self, screen):
        color = config.get('graph.edge.color')
        width = config.get('graph.edge.width')

        for edge in self.edges:
            a, b = map(self.nodes.get, edge)
            pygame.draw.line(screen, color, a.get_pos(), b.get_pos(), width=width)

    def _draw_nodes(self, screen):
        for node in self.nodes.values():
            node.draw(screen)
