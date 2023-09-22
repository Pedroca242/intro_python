import numpy as np

class Central_de_controle:

    def __init__(self, carros, clientes, ruas):
        self.carros = carros
        self.clientes = clientes
        self.delta_t = 0.1
        self.ruas = ruas

    def find_waypoint(self, carro, goal):
        way_point = carro.pos
        rua_proxima_y = self.ruas[np.absolute(self.ruas - goal[1]).argmin()]
        rua_proxima_x = self.ruas[np.absolute(self.ruas - goal[0]).argmin()]

        if carro.pos[0] in self.ruas and carro.pos[1] != rua_proxima_y:
            way_point = [carro.pos[0], rua_proxima_y]
        elif carro.pos[1] in self.ruas and carro.pos[0] != rua_proxima_x:
            way_point = [rua_proxima_x, carro.pos[1]]

        if carro.pos[0] == rua_proxima_x and carro.pos[1] == rua_proxima_y:
            way_point = goal

        return way_point

    def next_move(self, carro):
        delta_s = carro.speed*self.delta_t
        if not np.array_equal(carro.pos, carro.way_point):
            if carro.pos[0] < carro.way_point[0]:
                if delta_s > abs(carro.pos[0] - carro.way_point[0]):
                    carro.pos[0] = carro.way_point[0]
                else:
                    carro.pos[0] += delta_s
            elif carro.pos[0] > carro.way_point[0]:
                if delta_s > abs(carro.pos[0] - carro.way_point[0]):
                    carro.pos[0] = carro.way_point[0]
                else:
                    carro.pos[0] -= delta_s
            elif carro.pos[1] < carro.way_point[1]:
                if delta_s > abs(carro.pos[1] - carro.way_point[1]):
                    carro.pos[1] = carro.way_point[1]
                else:
                    carro.pos[1] += delta_s
            elif carro.pos[1] > carro.way_point[1]:
                if delta_s > abs(carro.pos[1] - carro.way_point[1]):
                    carro.pos[1] = carro.way_point[1]
                else:
                    carro.pos[1] -= delta_s

    def dont_collide(self, carro):
        for i in self.carros:
            if i.way_point is not None:
                distancia_way_point = abs(manhattan_distance(carro.pos, carro.way_point) - manhattan_distance(i.pos, i.way_point))

                if (carro.way_point == i.way_point and  distancia_way_point <= 2
                        and manhattan_distance(carro.pos, i.pos) <= 20 and carro.speed == i.default_speed
                        and i.speed == i.default_speed and carro != i and carro.pos[0] != i.pos[0] and carro.pos[1] != i.pos[1]):
                    carro.last_speed = carro.speed
                    carro.speed = carro.default_speed*0.50
                    for c in self.carros:
                        if c.pos[0] == carro.pos[0] or c.pos[1] == carro.pos[1] and manhattan_distance(c.pos, carro.pos) <= 15:
                            c.last_speed = c.speed
                            c.speed = carro.speed
                        else:
                            c.last_speed = c.speed
                            c.speed = c.default_speed
                # elif carro.pos[0] in self.ruas and carro.pos[0] == i.pos[0] and abs(carro.pos[1] - i.pos[1]) <= 5 and carro != i \
                #         and carro.speed == carro.default_speed and i.speed == i.default_speed:
                #     carro.last_speed = carro.speed
                #     carro.speed = carro.speed * 0.50
                # elif carro.pos[1] in self.ruas and carro.pos[1] == i.pos[1] and abs(carro.pos[0] - i.pos[0]) <= 5 and carro != i:
                #     carro.last_speed = carro.speed
                #     carro.speed = carro.speed * 0.50
                elif carro.way_point != i.way_point and carro.speed != carro.default_speed and carro != i:
                    carro.last_speed = carro.speed
                    carro.speed = carro.default_speed



def manhattan_distance(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])
