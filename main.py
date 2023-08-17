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

class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = manhattan_distance(pos, cliente1.goal)
        self.f = self.g + self.h

    def __lt__(self, other):  # Adicione este método para fazer a comparação funcionar
        return self.f < other.f

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
    open_list = PriorityQueue()
    start_node = Node(start)
    open_list.put((start_node.f, start_node))

    while not open_list.empty():
        _, current_node = open_list.get()

        if np.array_equal(current_node.pos, goal):
            path = []
            while current_node:
                path.insert(0, current_node.pos)
                current_node = current_node.parent
            return path

        new_pos = [[current_node.pos[0] - 1, current_node.pos[1]],
                   [current_node.pos[0] + 1, current_node.pos[1]],
                   [current_node.pos[0], current_node.pos[1] - 1],
                   [current_node.pos[0], current_node.pos[1] + 1]]

        for i in new_pos:
            if 0 <= i[0] < mapa.shape[0] and 0 <= i[1] < mapa.shape[1] and mapa[i[0], i[1]] == 0:
                new_node = Node(i, parent=current_node)
                open_list.put((new_node.f, new_node))
                mapa[i[0], i[1]] = 1  # Mark as visited

    return []

plt.ion()

cliente1 = cliente(321, np.array([40, 40]), np.array([2, 2]))
carro1 = carro(123, np.array([20, 80]))

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

