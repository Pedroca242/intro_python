import numpy as np

class Central_de_controle:

    def __init__(self, carros, clientes, ruas):
        self.carros = carros
        self.clientes = clientes
        self.delta_t = 0.1
        self.ruas = ruas

    def find_path(self, carro, goal):
        path = []
        current_pos = carro.pos
        flag = [True, True]
        
        delta_xy = carro.speed*self.delta_t

        while not np.array_equal(current_pos, goal):
            if current_pos[0] in self.ruas and flag[0]:
                rua_proxima = self.ruas[np.absolute(self.ruas - goal[1]).argmin()]
                if current_pos[1] < rua_proxima:
                    current_pos[1] += delta_xy
                    if carro.speed * self.delta_t > abs(current_pos[1] - rua_proxima):
                        current_pos[1] = rua_proxima
                elif current_pos[1] > self.ruas[np.absolute(self.ruas - goal[1]).argmin()]:
                    current_pos[1] -= delta_xy
                    if carro.speed * self.delta_t > abs(current_pos[1] - rua_proxima):
                        current_pos[1] = rua_proxima
                else:
                    while current_pos[0] != goal[0]:
                        if current_pos[0] < goal[0]:
                            current_pos[0] += delta_xy
                            if carro.speed * self.delta_t > abs(current_pos[0] - goal[0]):
                                current_pos[0] = goal[0]
                        elif current_pos[0] > goal[0]:
                            current_pos[0] -= delta_xy
                            if carro.speed * self.delta_t > abs(current_pos[0] - goal[0]):
                                current_pos[0] = goal[0]
                        path.append([current_pos[0], current_pos[1]])
                    flag[0] = False
            elif current_pos[1] in self.ruas and flag[1]:
                rua_proxima = self.ruas[np.absolute(self.ruas - goal[0]).argmin()]
                if current_pos[0] < rua_proxima:
                    current_pos[0] += delta_xy
                    if carro.speed * self.delta_t > abs(current_pos[0] - rua_proxima):
                        current_pos[0] = rua_proxima
                elif current_pos[0] > rua_proxima:
                    current_pos[0] -= delta_xy
                    if carro.speed * self.delta_t > abs(current_pos[0] - rua_proxima):
                        current_pos[0] = rua_proxima
                else:
                    while current_pos[1] != goal[1]:
                        if current_pos[1] < goal[1]:
                            current_pos[1] += delta_xy
                            if carro.speed * self.delta_t > abs(current_pos[1] - goal[1]):
                                current_pos[1] = goal[1]
                        elif current_pos[1] > goal[1]:
                            current_pos[1] -= delta_xy
                            if carro.speed * self.delta_t > abs(current_pos[1] - goal[1]):
                                current_pos[1] = goal[1]
                        path.append([current_pos[0], current_pos[1]])
                    flag[1] = False

            path.append([current_pos[0], current_pos[1]])
        return path

    def dont_collide(self):
        for i in self.carros:
            verify = []
            i_path = list(i.path)
            if i.pos[0] in self.ruas:
                rua_proxima = self.ruas[np.absolute(self.ruas - i.pos[1]).argmin()]
                for j in self.carros:
                    flag = False
                    j_path = list(j.path)
                    for p1, p2 in zip(i_path[i_path.index(i.pos): i_path.index(i.pos)+5], j_path[j_path.index(j.pos): i_path.index(j.pos)+5]):
                        if p1 == p2:
                            flag = True
                    if rua_proxima in j.pos and flag:
                        i.last_speed = i.speed
                        i.speed = i.speed - manhattan_distance(i.pos, j.pos)*0.5
                        flag = False
                    else:
                        verify.append(True)
                if any(verify):
                    i.last_speed = i.speed
                    i.speed = i.default_speed






def manhattan_distance(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])