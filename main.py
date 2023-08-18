import numpy as np
import time
import matplotlib.pyplot as plt
from queue import PriorityQueue


class cliente:
    def __init__(self, id, pos, goal):
        self.id = id
        self.pos = pos
        self.goal = goal

class carro:
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos

def draw_map():
    mapa = np.ones((101, 101))
    figure, ax = plt.subplots(figsize=(5,5))
    for i in range(0, 120, 20):
        mapa[i, :] = 0
        mapa[:, i] = 0
    ax.imshow(mapa, cmap = 'gray_r', vmin = 0, vmax = 1,origin='lower')
    return figure, ax, mapa

def update_graph(new_pos):
    poscarro.set_offsets(np.c_[new_pos[0], new_pos[1]])
    figure.canvas.draw()
    figure.canvas.flush_events()

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

plt.ion()

cliente1 = cliente(321, np.array([100, 100]), np.array([2, 2]))
carro1 = carro(123, np.array([7, 0]))

flag = True

figure, ax, mapa = draw_map()

poscliente = ax.scatter(cliente1.pos[0], cliente1.pos[1], s = 20, zorder = 2)
poscarro = ax.scatter(carro1.pos[0], carro1.pos[1], s = 20, zorder = 2)

carro_path = find_path(carro1.pos, cliente1.pos, mapa)

while flag:
    for i in carro_path:
        carro1.pos = np.array(i)
        update_graph(i)
        time.sleep(0.1)

