import numpy as np

class Central_de_controle:

    def __init__(self, carros, clientes, ruas):
        self.carros = carros
        self.clientes = clientes
        self.ruas = ruas

    def find_path(self, start, goal):
        path = []
        current_pos = start
        flag = [True, True]

        while not np.array_equal(current_pos, goal):
            if current_pos[0] in self.ruas and flag[0]:
                if current_pos[1] < self.ruas[np.absolute(self.ruas - goal[1]).argmin()]:
                    current_pos[1] += 1
                elif current_pos[1] > self.ruas[np.absolute(self.ruas - goal[1]).argmin()]:
                    current_pos[1] -= 1
                else:
                    while current_pos[0] != goal[0]:
                        if current_pos[0] < goal[0]:
                            current_pos[0] += 1
                        elif current_pos[0] > goal[0]:
                            current_pos[0] -= 1
                        path.append([current_pos[0], current_pos[1]])
                    flag[0] = False
            elif current_pos[1] in self.ruas and flag[1]:
                if current_pos[0] < self.ruas[np.absolute(self.ruas - goal[0]).argmin()]:
                    current_pos[0] += 1
                elif current_pos[0] > self.ruas[np.absolute(self.ruas - goal[0]).argmin()]:
                    current_pos[0] -= 1
                else:
                    while current_pos[1] != goal[1]:
                        if current_pos[1] < goal[1]:
                            current_pos[1] += 1
                        elif current_pos[1] > goal[1]:
                            current_pos[1] -= 1
                        path.append([current_pos[0], current_pos[1]])
                    flag[1] = False

            path.append([current_pos[0], current_pos[1]])
        print(path)
        return path