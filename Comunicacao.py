import numpy as np

class Comunicacao:

    def __init__(self, central, carros):
        self.central = central
        self.carros = carros

    def send_path(self):
        for i in self.central.carros:
            if i.path is None and not i.passageiro and i.cliente:
                i.path = iter(self.central.find_path(i.pos, i.cliente.pos))
            elif i.passageiro and i.path is None:
                i.cliente.remove_graph()
                i.path = iter(self.central.find_path(i.pos, i.cliente.goal))



    def new_client(self):
        for cliente in self.central.clientes:
            if cliente.need_ride:
                carros_disponiveis = [carro for carro in self.central.carros if carro.cliente is None]
                if carros_disponiveis:
                    carro_escolhido = np.random.choice(carros_disponiveis)
                    carro_escolhido.cliente = cliente
                    cliente.need_ride = False