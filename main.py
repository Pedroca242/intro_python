import numpy as np
import matplotlib.pyplot as plt
from Setup import Setup
from Comunicacao import MQTTCommunicator
import logging

def draw_map(mapa):
    figure, ax = plt.subplots(figsize=(5,5))
    ax.imshow(mapa, cmap = 'gray_r', vmin = 0, vmax = 1,origin='lower')
    return figure, ax

n_ruas = 6
n_carros = n_ruas - 1

ruas = np.array([i for i in range(0, n_ruas*20, 20)])

logging.basicConfig(level=logging.INFO)

config = Setup(n_carros, ruas)
config.comunicador = MQTTCommunicator("Config_carros", "localhost")
config.comunicador.start()


plt.ion()
figure, ax = draw_map(config.mapa)

carros = config.carros
clientes = config.gerar_clientes(n_carros)

for carro, cliente, n in zip(carros, clientes, range(n_carros)):
    cliente.create_point(ax)
    cliente.comunicador = MQTTCommunicator(f'cliente{n}', "localhost")

    carro.create_point(ax)
    carro.comunicador = MQTTCommunicator(f'carro{n}', "localhost")

for carro, cliente, n in zip(carros, clientes, range(n_carros)):
    cliente.comunicador.start()
    carro.comunicador.start()

    cliente.subscribe("cliente")
    carro.subscribe("carro")



    cliente.publish

while True:
    pass

# while True:
#     config.new_goal()
#     for i in clientes:
#         if i.need_ride == True:
#             i.comunicador.publish("central", "need ride")
#
#     for carro in carros:
#         if carro.cliente is not None:
#             carro.comunicador.publish("central", "need move")
#         else:
#             carro.comunicador.publish("central", "no client")
#
#         i.update_graph()
#         print(i.cliente)
#
#     figure.canvas.draw()
#     figure.canvas.flush_events()

