import numpy as np
import time
import matplotlib.pyplot as plt

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

def find_path(start, goal):
    path = []
    current_pos = start
    min_distance_value = manhattan_distance(current_pos, goal)

    while manhattan_distance(current_pos, goal):
        new_pos = [[current_pos[0] - 1, current_pos[1]], [current_pos[0] + 1, current_pos[1]], [current_pos[0], current_pos[1] - 1], [current_pos[0], current_pos[1] + 1]]
        for i in new_pos:
            if manhattan_distance(i, goal) < min_distance_value:
                min_distance_value = manhattan_distance(i, goal)
                path.append(i)
                current_pos = i
    return path

plt.ion()

cliente1 = cliente(321, np.array([80, 80]), np.array([2, 2]))
carro1 = carro(123, np.array([40, 40]))

flag = True

figure, ax, mapa = draw_map()

poscliente = ax.scatter(cliente1.pos[0], cliente1.pos[1], s = 20, zorder = 2)
poscarro = ax.scatter(carro1.pos[0], carro1.pos[1], s = 20, zorder = 2)

carro_path = find_path(carro1.pos, cliente1.pos)

while flag:
    for i in carro_path:
        update_graph(i)
        time.sleep(0.1)


