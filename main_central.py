from Central_de_controle import Central_de_controle
import logging
from Comunicacao import MQTTCommunicator
from Setup import Setup
import numpy as np
import matplotlib.pyplot as plt
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




while True:
    if "Setup" in setup.comunicador.info:
        tipo = setup.comunicador.info.split('/')[1]
        pos = setup.comunicador.info.split('/')[2]
        if "carro" in tipo:
            speed = setup.comunicador.info.split('/')[3]
            carros[int(tipo[-1])] = Carro(pos, speed)
        if "cliente" in tipo:
            goal = setup.comunicador.info.split('/')[3]
            clientes[int(tipo[-1])] = Cliente(pos, goal)






