import numpy as np

class Central_de_controle:

    def __init__(self, comunicador, ruas):
        self.delta_t = 0.1
        self.ruas = ruas
        self.comunicador = comunicador

    def find_waypoint(self,pos1, goal):
        way_point = pos1
        rua_proxima_y = self.ruas[np.absolute(self.ruas - goal[1]).argmin()]
        rua_proxima_x = self.ruas[np.absolute(self.ruas - goal[0]).argmin()]

        if pos1[0] in self.ruas and pos1[1] != rua_proxima_y:
            way_point = [pos1[0], rua_proxima_y]
        elif pos1[1] in self.ruas and pos1[0] != rua_proxima_x:
            way_point = [rua_proxima_x, pos1[1]]

        if pos1[0] == rua_proxima_x and pos1[1] == rua_proxima_y:
            way_point = goal

        return way_point

def manhattan_distance(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])
