import numpy as np

class Carro:

    def __init__(self, pos, speed=10, passageiro=False):
        self.pos = pos
        self.cliente = None
        self.passageiro = passageiro
        self.speed = speed
        self.default_speed = 10
        self.last_speed = self.speed
        self.way_point = None
        self.have_point = None
        self.comunicador = None
        self.delta_t = 0.1

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

    def send_move(self):
            if self.cliente is not None:
                if self.pos == self.cliente.pos and self.pos != self.cliente.goal:
                    self.passageiro = True

                if self.passageiro == True:
                    self.cliente.pos = self.pos
                else:
                    self.cliente.pos = self.cliente.pos.copy()

                if self.pos == self.cliente.goal and self.cliente.pos == self.cliente.goal:
                    #self.cliente.need_ride = True
                    self.cliente = None
                    self.passageiro = False
                self.next_move()

    def next_move(self):
        delta_s = self.speed*self.delta_t
        if not np.array_equal(self.pos, self.way_point):
            if self.pos[0] < self.way_point[0]:
                if delta_s > abs(self.pos[0] - self.way_point[0]):
                    self.pos[0] = self.way_point[0]
                else:
                    self.pos[0] += delta_s
            elif self.pos[0] > self.way_point[0]:
                if delta_s > abs(self.pos[0] - self.way_point[0]):
                    self.pos[0] = self.way_point[0]
                else:
                    self.pos[0] -= delta_s
            elif self.pos[1] < self.way_point[1]:
                if delta_s > abs(self.pos[1] - self.way_point[1]):
                    self.pos[1] = self.way_point[1]
                else:
                    self.pos[1] += delta_s
            elif self.pos[1] > self.way_point[1]:
                if delta_s > abs(self.pos[1] - self.way_point[1]):
                    self.pos[1] = self.way_point[1]
                else:
                    self.pos[1] -= delta_s