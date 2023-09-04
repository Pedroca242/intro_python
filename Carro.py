import numpy as np

class Carro:

    def __init__(self, pos, passageiro=False):
        self.pos = pos
        self.cliente = None
        self.passageiro = passageiro
        self.path = None
        self.have_point = None

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='blue')
        self.have_point = True
        return self.pos_graph

    def update_graph(self, figure):
        if self.path:
            new_pos = next(self.path)
            self.pos = new_pos
            self.pos_graph.set_offsets(np.c_[new_pos[0], new_pos[1]])
            figure.canvas.draw()
            figure.canvas.flush_events()

    def remove_graph(self, situation):
        if situation == None:
            self.pos_graph.remove()