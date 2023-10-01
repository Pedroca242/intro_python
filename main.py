import numpy as np
import matplotlib.pyplot as plt
from Setup import Setup
from Comunicacao import MQTTCommunicator
import logging
import json
import time

def draw_map(mapa):
    figure, ax = plt.subplots(figsize=(5,5))
    ax.imshow(mapa, cmap = 'gray_r', vmin = 0, vmax = 1,origin='lower')
    return figure, ax

with open('config.json', 'r') as arquivo_config:
    config = json.load(arquivo_config)

n_ruas = config["n_ruas"]
n_carros = config["n_carros"]

ruas = np.array([i for i in range(0, n_ruas*20, 20)])





logging.basicConfig(level=logging.INFO)

setup = Setup(n_carros, ruas)
setup.comunicador = MQTTCommunicator("Config_carros", "localhost")
setup.comunicador.start()


plt.ion()
figure, ax = draw_map(setup.mapa)

carros = setup.carros
clientes = setup.gerar_clientes(n_carros)

for carro, cliente, n in zip(carros, clientes, range(n_carros)):
    cliente.create_point(ax)
    cliente.comunicador = MQTTCommunicator(f'cliente{n}', "localhost")

    carro.create_point(ax)
    carro.comunicador = MQTTCommunicator(f'carro{n}', "localhost")

for carro, cliente, n in zip(carros, clientes, range(n_carros)):
    cliente.comunicador.start()
    carro.comunicador.start()

    cliente.comunicador.subscribe(f"{cliente.comunicador.client_id}")
    carro.comunicador.subscribe(f"{carro.comunicador.client_id}")

for carro in carros:
    carro.comunicador.publish("central", f'Setup/{carro.comunicador.client_id}/{carro.pos}/{carro.speed}')
    time.sleep(0.1)

for cliente in clientes:
    cliente.comunicador.publish("central", f'Setup/{cliente.comunicador.client_id}/{cliente.pos}/{cliente.goal}')
    time.sleep(0.1)

n = 0
while True:
    for carro in carros:
        if "cliente" in carro.comunicador.info:
            index = int(carro.comunicador.info.split('/')[-1])
            carro.cliente = clientes[index]


        if "way_point" in carro.comunicador.info:
            way_point = eval(carro.comunicador.info.split('/')[-1])
            carro.way_point = way_point

        if carro.way_point is not None:
            if carro.pos == carro.way_point:
                carro.comunicador.publish("central", f'{carro.pos}')
            if carro.pos == carro.cliente.goal:
                setup.new_goal()
                for cliente in clientes:
                    cliente.comunicador.publish("central", f'cliente{cliente.comunicador.client_id[-1]}/new_goal/{cliente.goal}')
                    cliente.show_point()
            carro.send_move()
        carro.update_graph()
        if carro.passageiro and carro.cliente is not None:
            carro.cliente.remove_graph()
            carro.cliente.pos = carro.pos

        n += 1
        if n == 100:
            for cliente in clientes:
                if cliente.pos == cliente.goal:
                    cliente.need_ride = True
                    cliente.comunicador.publish("central", f'cliente{cliente.comunicador.client_id[-1]}/need_ride')






    figure.canvas.draw()
    figure.canvas.flush_events()







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
#
#         print(i.cliente)
#

