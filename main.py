import numpy as np
import matplotlib.pyplot as plt
from Setup import Setup
from Comunicacao import Comunicacao
from Central_de_controle import Central_de_controle

def draw_map(mapa):
    figure, ax = plt.subplots(figsize=(5,5))
    ax.imshow(mapa, cmap = 'gray_r', vmin = 0, vmax = 1,origin='lower')
    return figure, ax

plt.ion()

n_ruas = 6

ruas = np.array([i for i in range(0, n_ruas*20, 20)])

config = Setup(5, ruas)
figure, ax = draw_map(config.mapa)

central = Central_de_controle(config.carros, config.gerar_clientes(5), ruas=ruas)
comms = Comunicacao(central, config.carros)


for i, j in zip(central.clientes, central.carros):
    i.create_point(ax)
    j.create_point(ax)

comms.new_client()

# print(central.carros[0].pos, central.clientes[0].pos)
# print(central.find_waypoint(central.carros[0], central.clientes[0].pos))
# central.carros[0].way_point = central.find_waypoint(central.carros[0], central.clientes[0].pos)
# central.next_move(central.carros[0])
# print(central.carros[0].pos)
# print(central.find_waypoint(central.carros[0], central.clientes[0].pos))

while True:
    comms.send_waypoint()
    comms.send_move()
    
    for i in central.carros:
        i.update_graph()
        print(i.pos, i.way_point)

    figure.canvas.draw()
    figure.canvas.flush_events()

    test = [i.passageiro for i in central.carros]
    print(test)
