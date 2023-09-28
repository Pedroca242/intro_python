import numpy as np

class Cliente:
    def __init__(self, pos, goal, embarque=None):
        self.pos = pos
        self.goal = goal
        self.need_ride = True
        self.embarque = embarque
        self.have_point = False
        self.comunicador = None

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='red')
        return self.pos_graph

    def show_point(self):
        self.pos_graph.set_offsets(np.c_[self.pos[0], self.pos[1]])
        self.pos_graph.set_visible(True)

    def remove_graph(self):
        self.pos_graph.set_visible(False)
