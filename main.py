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

ruas = np.array([0, 20, 40, 60, 80, 100])

config = Setup(5, ruas)
figure, ax = draw_map(config.mapa)

central = Central_de_controle(config.carros, config.gerar_clientes(5), ruas=ruas)
comms = Comunicacao(central, config.carros)


for i, j in zip(central.clientes, central.carros):
    i.create_point(ax)
    j.create_point(ax)

comms.new_client()

while True:
    comms.send_path()
    
    for i in central.carros:
        i.update_graph()

    figure.canvas.draw()
    figure.canvas.flush_events()

    test = [i.passageiro for i in central.carros]
    print(test)
