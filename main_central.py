from Central_de_controle import Central_de_controle
import logging
from Comunicacao import MQTTCommunicator
from Setup import Setup
import numpy as np
import time
from Carro import Carro
from Cliente import Cliente
import json

with open('config.json', 'r') as arquivo_config:
    config = json.load(arquivo_config)

n_ruas = config["n_ruas"]
n_carros = config["n_carros"]

ruas = np.array([i for i in range(0, n_ruas*20, 20)])

carros = [0 for n in range(n_carros)]
clientes = [0 for n in range(n_carros)]

objetos = {}


logging.basicConfig(level=logging.INFO)

setup = Setup(n_carros, ruas)
setup.comunicador = MQTTCommunicator("Config_central", "localhost")
setup.comunicador.start()


setup.comunicador.subscribe("central")

while True:
    if "Setup" in setup.comunicador.info:
        tipo = setup.comunicador.info.split('/')[1]
        pos = eval(setup.comunicador.info.split('/')[2])

        if "carro" in tipo and 0 in carros:
            speed = eval(setup.comunicador.info.split('/')[-1])
            carros[int(tipo[-1])] = tipo
        if "cliente" in tipo and 0 in clientes:
            goal = eval(setup.comunicador.info.split('/')[-1])
            clientes[int(tipo[-1])] = tipo
    if 0 not in carros and 0 not in clientes:
        break

# for i in carros:
#     random_client = np.random.choice(clientes)
#     objetos[i] = random_client
#     clientes.remove(random_client)
#
# print(objetos)

central = Central_de_controle(MQTTCommunicator("central", "localhost"), ruas)
central.comunicador.start()
central.comunicador.subscribe("central")

free_cars = [car for car in carros]
current_clients = []



while True:
    if "need_car" in central.comunicador.info:
        if len(free_cars) != 0 and central.comunicador.info.split('/')[1] not in current_clients:
            client_id = central.comunicador.info.split('/')[1]
            random_car = np.random.choice(free_cars)
            free_cars.remove(random_car)
            current_clients.append(client_id)
            central.comunicador.publish(random_car, f"cliente/{client_id}")

    if "need_waypoint" in central.comunicador.info:
        car_pos = eval(central.comunicador.info.split('/')[-2])
        car_goal = eval(central.comunicador.info.split('/')[-1])
        way_point = central.find_waypoint(car_pos, car_goal)
        central.comunicador.publish(central.comunicador.info.split('/')[0], f'way_point/{way_point}')
        time.sleep(0.01)

    if "livre" in central.comunicador.info:
        if central.comunicador.info.split('/')[0] not in free_cars and  central.comunicador.info.split('/')[1] in current_clients:
            free_cars.append(central.comunicador.info.split('/')[0])
            current_clients.remove(central.comunicador.info.split('/')[1])
