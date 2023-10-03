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

n = [100 for i in range(len(clientes))]


while True:
    for cliente, j in zip(clientes, range(len(clientes))):
        if cliente.need_ride and not cliente.have_point:
            time.sleep(0.01)
            cliente.show_point()
        if n[j] == 100:
            n[j] = 0
            setup.new_goal(cliente)
            cliente.comunicador.publish("central", f"need_car/{cliente.comunicador.client_id}")
            time.sleep(0.1)
        n[j] += 1


    for carro in carros:
        if "cliente" in carro.comunicador.info:
            selected_id = carro.comunicador.info.split('/')[-1]
            selected_client = None
            for i in clientes:
                if i.comunicador.client_id == selected_id:
                    selected_client = i
            carro.cliente = selected_client
            if selected_client is not None:
                selected_client.need_ride = False

        if (carro.way_point is None or carro.pos == carro.way_point) and carro.cliente is not None:
            if not carro.passageiro:
                carro.comunicador.publish("central", f"{carro.comunicador.client_id}/need_waypoint/{carro.pos}/{carro.cliente.pos}")
            else:
                carro.comunicador.publish("central", f"{carro.comunicador.client_id}/need_waypoint/{carro.pos}/{carro.cliente.goal}")

        if "way_point" in carro.comunicador.info:
            way_point = eval(carro.comunicador.info.split('/')[-1])
            carro.way_point = way_point

        if carro.cliente is not None:
            if carro.pos == carro.cliente.goal and carro.cliente.pos == carro.cliente.goal:
                carro.comunicador.publish("central", f"{carro.comunicador.client_id}/{carro.cliente.comunicador.client_id}/livre")
                time.sleep(0.1)


        if carro.passageiro:
            carro.cliente.have_point = False
            carro.cliente.remove_graph()

        if carro.way_point is not None:
            carro.send_move()
            carro.update_graph()

    figure.canvas.draw()
    figure.canvas.flush_events()
