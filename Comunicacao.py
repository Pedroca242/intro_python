import numpy as np

class Comunicacao:

    def __init__(self, central, carros):
        self.central = central
        self.carros = carros

    def send_waypoint(self):
        for i in self.central.carros:
            if i.cliente and not i.passageiro:
                i.way_point = self.central.find_waypoint(i, i.cliente.pos)
            elif i.cliente and i.passageiro:
                i.way_point = self.central.find_waypoint(i, i.cliente.goal)
            else:
                i.way_point = i.pos

    def send_move(self):
        for i in self.central.carros:
            if i.way_point != i.pos and i.cliente is not None:
                self.central.next_move(i)
                if i.pos == i.cliente.pos:
                    i.passageiro = True
                if i.pos == i.cliente.goal:
                    i.cliente = None
                    i.passageiro = False



    def new_client(self):
        for cliente in self.central.clientes:
            if cliente.need_ride:
                carros_disponiveis = [carro for carro in self.central.carros if carro.cliente is None]
                if carros_disponiveis:
                    carro_escolhido = np.random.choice(carros_disponiveis)
                    carro_escolhido.cliente = cliente
                    cliente.need_ride = False