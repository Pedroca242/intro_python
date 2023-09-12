import numpy as np

class Carro:

    def __init__(self, pos, passageiro=False):
        self.pos = pos
        self.cliente = None
        self.passageiro = passageiro
        self.speed = 20
        self.default_speed = 10
        self.last_speed = self.speed
        self.path = None
        self.have_point = None

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='blue')
        self.have_point = True
        return self.pos_graph

    def update_graph(self):
        if self.path is not None:
            try:
                new_pos = next(self.path)
            except StopIteration:
                new_pos = self.pos
                self.path = None

            self.pos = new_pos

            if self.cliente is not None:
                if self.pos == self.cliente.pos:
                    self.passageiro = True

                if self.passageiro:
                    self.cliente.pos = self.pos

                if self.pos == self.cliente.goal:
                    self.cliente.need_ride = True
                    self.cliente = None
                    self.passageiro = False

            if self.have_point:
                self.pos_graph.set_offsets(np.c_[new_pos[0], new_pos[1]])


    def remove_graph(self, situation):
        if situation == None:
            self.pos_graph.remove()