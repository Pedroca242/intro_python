import numpy as np

class Cliente:
    def __init__(self, pos, goal, embarque=None, chegada=None):
        self.pos = pos
        self.goal = goal
        self.need_ride = True
        self.embarque = embarque

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='red')
        return self.pos_graph

    def remove_graph(self):
        self.pos_graph.set_visible(False)
