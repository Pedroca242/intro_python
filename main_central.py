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


logging.basicConfig(level=logging.INFO)

setup = Setup(n_carros, ruas)
setup.comunicador = MQTTCommunicator("Config_central", "localhost")
setup.comunicador.start()


setup.comunicador.subscribe("central")


flag = False

while True:
    if "Setup" in setup.comunicador.info:
        tipo = setup.comunicador.info.split('/')[1]
        pos = eval(setup.comunicador.info.split('/')[2])

        if "carro" in tipo and 0 in carros:
            speed = eval(setup.comunicador.info.split('/')[-1])
            carros[int(tipo[-1])] = Carro(pos, speed)
        if "cliente" in tipo and 0 in clientes:
            goal = eval(setup.comunicador.info.split('/')[-1])
            clientes[int(tipo[-1])] = Cliente(pos, goal)

    if 0 not in carros and 0 not in clientes:
        if not flag:
            central = Central_de_controle(carros, clientes, MQTTCommunicator("central", "localhost"), ruas)
            central.comunicador.start()
            central.comunicador.subscribe("central")
            flag = True
        else:
            for i in carros:
                if i.cliente is None:
                    central.new_client(i)
                    if i.cliente is not None:
                        central.comunicador.publish(f"carro{carros.index(i)}", f'cliente/{clientes.index(i.cliente)}')
                    time.sleep(0.1)

                if "new_goal" in central.comunicador.info:
                    index = int(central.comunicador.info.split('/')[0][-1])
                    clientes[index].goal = eval(central.comunicador.info.split('/')[-1])

                if "need_ride" in central.comunicador.info:
                    index = int(central.comunicador.info.split('/')[0][-1])
                    clientes[index].need_ride = True

                if i.way_point is None or (str(i.pos) == central.comunicador.info):
                    if i.cliente is not None:
                        central.send_waypoint(i)
                    central.comunicador.publish(f"carro{carros.index(i)}", f'way_point/{i.way_point}')
                    time.sleep(0.1)
                else:
                    central.send_move(i)














