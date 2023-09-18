import numpy as np

class Comunicacao:

    def __init__(self, central, carros):
        self.central = central
        self.carros = carros

    def send_waypoint(self, carro):
        if not carro.passageiro:
            carro.way_point = self.central.find_waypoint(carro, carro.cliente.pos)
        elif carro.passageiro:
            carro.way_point = self.central.find_waypoint(carro, carro.cliente.goal)

    def send_move(self):
        for i in self.central.carros:
            if i.cliente is not None:
                if i.way_point is None:
                    self.send_waypoint(i)
                if i.pos == i.cliente.pos:
                    i.passageiro = True
                    i.cliente.remove_graph()
                if i.pos == i.cliente.goal:
                    i.cliente = None
                    i.passageiro = False
                if i.pos == i.way_point and i.cliente is not None:
                    self.send_waypoint(i)
                self.central.next_move(i)




    def new_client(self):
        for cliente in self.central.clientes:
            if cliente.need_ride:
                carros_disponiveis = [carro for carro in self.central.carros if carro.cliente is None]
                if carros_disponiveis:
                    carro_escolhido = np.random.choice(carros_disponiveis)
                    carro_escolhido.cliente = cliente
                    cliente.need_ride = False