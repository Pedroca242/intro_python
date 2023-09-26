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
                i.show_point()
                if i.way_point is None:
                    self.send_waypoint(i)

                if i.pos == i.cliente.pos and i.pos != i.cliente.goal:
                    i.passageiro = True

                if i.passageiro == True:
                    i.cliente.pos = i.pos
                    i.cliente.remove_graph()
                else:
                    i.cliente.pos = i.cliente.pos.copy()
                    i.cliente.show_point()

                if i.pos == i.cliente.goal and i.cliente.pos == i.cliente.goal:
                    i.cliente.need_ride = True
                    i.cliente = None
                    i.passageiro = False


                if i.pos == i.way_point and i.cliente is not None:
                    self.send_waypoint(i)
                self.central.dont_collide(i)
                self.central.next_move(i)
            # else:
            #     i.remove_graph()

    def new_client(self):
        for cliente in self.central.clientes:
            if cliente.need_ride:
                carros_disponiveis = [carro for carro in self.central.carros if carro.cliente is None]
                if carros_disponiveis:
                    carro_escolhido = np.random.choice(carros_disponiveis)
                    carro_escolhido.cliente = cliente
                    cliente.need_ride = False