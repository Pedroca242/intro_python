import numpy as np
import matplotlib.pyplot as plt

class Cliente:
    def __init__(self, pos, goal, embarque=None, chegada=None):
        self.pos = pos
        self.goal = goal
        self.embarque = embarque
        self.chegada = chegada

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='red')
        return self.pos_graph
    def update_graph(self, figure, new_pos, ax):
        self.pos_graph.set_offsets(np.c_[new_pos[0], new_pos[1]])
        figure.canvas.draw()
        figure.canvas.flush_events()

    def remove_graph(self):
        if self.embarque == True:
            self.pos_graph.remove()

class Carro:
    def __init__(self, pos, cliente=None, passageiro=False):
        self.pos = pos
        self.cliente = cliente
        self.passageiro = passageiro
        self.have_point = None

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='blue')
        self.have_point = True
        return self.pos_graph

    def update_graph(self, figure, new_pos, ax):
        self.pos_graph.set_offsets(np.c_[new_pos[0], new_pos[1]])
        figure.canvas.draw()
        figure.canvas.flush_events()

    def remove_graph(self, situation):
        if situation == None:
            self.pos_graph.remove()

class Setup:

    def __init__(self, n_carros, ruas):
        self.mapa = self.gerar_mapa()
        self.carros = [Carro(random_pos(self.mapa)) for i in range(n_carros)]
        self.ruas = ruas

    def gerar_clientes(self, max_clientes):
        n_clientes = np.random.randint(max_clientes)
        clientes = [Cliente(random_pos(self.mapa), random_pos(self.mapa)) for i in range(n_clientes)]
        return clientes

    def gerar_mapa(self):
        mapa = np.ones((101, 101))
        for i in self.ruas:
            mapa[i, :] = 0
            mapa[:, i] = 0
        return mapa


class Central_de_controle:

    def __init__(self, carros, clientes, ruas):
        self.carros = carros
        self.clientes = clientes
        self.ruas = ruas

    def find_path(self, start, goal):
        path = []
        current_pos = start
        flag = [True, True]

        while not np.array_equal(current_pos, goal):
            if current_pos[0] in self.ruas and flag[0]:
                if current_pos[1] < self.ruas[np.absolute(self.ruas - goal[1]).argmin()]:
                    current_pos[1] += 1
                elif current_pos[1] > self.ruas[np.absolute(self.ruas - goal[1]).argmin()]:
                    current_pos[1] -= 1
                else:
                    while current_pos[0] != goal[0]:
                        if current_pos[0] < goal[0]:
                            current_pos[0] += 1
                        elif current_pos[0] > goal[0]:
                            current_pos[0] -= 1
                        path.append([current_pos[0], current_pos[1]])
                    flag[0] = False
            elif current_pos[1] in self.ruas and flag[1]:
                if current_pos[0] < self.ruas[np.absolute(self.ruas - goal[0]).argmin()]:
                    current_pos[0] += 1
                elif current_pos[0] > self.ruas[np.absolute(self.ruas - goal[0]).argmin()]:
                    current_pos[0] -= 1
                else:
                    while current_pos[1] != goal[1]:
                        if current_pos[1] < goal[1]:
                            current_pos[1] += 1
                        elif current_pos[1] > goal[1]:
                            current_pos[1] -= 1
                        path.append([current_pos[0], current_pos[1]])
                    flag[1] = False

            path.append([current_pos[0], current_pos[1]])
        return path
    

def draw_map(mapa):
    figure, ax = plt.subplots(figsize=(5,5))
    ax.imshow(mapa, cmap = 'gray_r', vmin = 0, vmax = 1,origin='lower')
    return figure, ax

def manhattan_distance(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])



def random_pos(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])

    while True:
        linha_aleatoria = np.random.randint(0, linhas - 1)
        coluna_aleatoria = np.random.randint(0, colunas - 1)

        if matriz[linha_aleatoria][coluna_aleatoria] == 0:
            return [linha_aleatoria, coluna_aleatoria]

plt.ion()

ruas = np.array([0, 20, 40, 60, 80, 100])

config = Setup(5, ruas)
figure, ax = draw_map(config.mapa)

central = Central_de_controle(config.carros, config.gerar_clientes(5), ruas=ruas)





