from Central_de_controle import Central_de_controle
import logging
from Comunicacao import MQTTCommunicator
from Setup import Setup
import numpy as np
import matplotlib.pyplot as plt


n_ruas = 6
n_carros = n_ruas - 1

ruas = np.array([i for i in range(0, n_ruas*20, 20)])

logging.basicConfig(level=logging.INFO)


config = Setup(n_carros, ruas)
config.comunicador = MQTTCommunicator("Config_central", "localhost")
config.comunicador.start()

central = Central_de_controle(config.carros, config.gerar_clientes(n_carros), MQTTCommunicator("central", "localhost"), ruas=ruas)
central.comunicador.start()
central.comunicador.subscribe("central")

while True:
    pass
