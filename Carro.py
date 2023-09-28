import numpy as np

class Carro:

    def __init__(self, pos, passageiro=False):
        self.id = np.random.randint(134256)
        self.pos = pos
        self.cliente = None
        self.passageiro = passageiro
        self.speed = 10
        self.default_speed = 10
        self.last_speed = self.speed
        self.way_point = None
        self.have_point = None
        self.comunicador = None

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='blue')
        self.have_point = True
        return self.pos_graph

    def update_graph(self):
        self.pos_graph.set_offsets(np.c_[self.pos[0], self.pos[1]])

    def show_point(self):
        self.pos_graph.set_offsets(np.c_[self.pos[0], self.pos[1]])
        self.pos_graph.set_visible(True)

    def remove_graph(self):
        self.pos_graph.set_visible(False)