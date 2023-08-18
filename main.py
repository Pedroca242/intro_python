import numpy as np
import time
import matplotlib.pyplot as plt

class cliente:
    def __init__(self, id, pos, goal):
        self.id = id
        self.pos = pos
        self.goal = goal

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='red')
        return self.pos_graph
    def update_graph(self, new_pos, ax):
        self.pos_graph.set_offsets(np.c_[new_pos[0], new_pos[1]])
        figure.canvas.draw()
        figure.canvas.flush_events()

class carro:
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos

    def create_point(self, ax):
        self.pos_graph = ax.scatter(self.pos[0], self.pos[1], s=20, zorder=2, c='blue')
        return self.pos_graph

    def update_graph(self, figure, new_pos, ax):
        self.pos_graph.set_offsets(np.c_[new_pos[0], new_pos[1]])
        figure.canvas.draw()
        figure.canvas.flush_events()

def draw_map():
    mapa = np.ones((101, 101))
    figure, ax = plt.subplots(figsize=(5,5))
    for i in range(0, 120, 20):
        mapa[i, :] = 0
        mapa[:, i] = 0
    ax.imshow(mapa, cmap = 'gray_r', vmin = 0, vmax = 1,origin='lower')
    return figure, ax, mapa

def manhattan_distance(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

def find_path(start, goal, mapa):
    path = []
    current_pos = start
    ruas = [0, 20, 40, 60, 80, 100]
    flag = [True, True]

    while not np.array_equal(current_pos, goal):
        if current_pos[0] in ruas and flag[0]:
            if current_pos[1] < ruas[np.absolute(ruas - goal[1]).argmin()]:
                current_pos[1] += 1
            elif current_pos[1] > ruas[np.absolute(ruas - goal[1]).argmin()]:
                current_pos[1] -= 1
            else:
                while current_pos[0] != goal[0]:
                    if current_pos[0] < goal[0]:
                        current_pos[0] += 1
                    elif current_pos[0] > goal[0]:
                        current_pos[0] -= 1
                    path.append([current_pos[0], current_pos[1]])
                flag[0] = False
        elif current_pos[1] in ruas and flag[1]:
            if current_pos[0] < ruas[np.absolute(ruas - goal[0]).argmin()]:
                current_pos[0] += 1
            elif current_pos[0] > ruas[np.absolute(ruas - goal[0]).argmin()]:
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

def random_pos(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])

    while True:
        linha_aleatoria = np.random.randint(0, linhas - 1)
        coluna_aleatoria = np.random.randint(0, colunas - 1)

        if matriz[linha_aleatoria][coluna_aleatoria] == 0:
            return [linha_aleatoria, coluna_aleatoria]

plt.ion()

cliente1 = cliente(321, np.array([45, 60]), np.array([2, 2]))
flag = True

figure, ax, mapa = draw_map()

n_carros = 3
carros = []
carros_path = []

for i in range(n_carros):
    carros.append(carro(np.random.randint(100), random_pos(mapa)))

cliente1.create_point(ax)
for n, j in enumerate(carros):
    j.create_point(ax)
    carros_path.append(find_path(carros[n].pos, cliente1.pos, mapa))

while flag:
    for i, j in zip(carros, carros_path):
        for k in j:
            i.pos = np.array(k)
            i.update_graph(figure, k, ax)
            time.sleep(0.1)

